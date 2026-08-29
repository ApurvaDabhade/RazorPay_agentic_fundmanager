"""
sentinel.scenario_simulator
What-If / Scenario Simulator for Predictive Project Planning
"""

import copy
from typing import Dict, List, Any, Optional
from .models import ProjectState, ScenarioResult, TaskStatus
from .predictive_engine import PredictiveRiskEngine
from .dependency_engine import DependencyEngine


class ScenarioSimulator:
    """Simulates hypothetical project perturbations and quantifies timeline and budget deltas."""

    def __init__(self, state: ProjectState):
        self.state = state

    def _get_baseline_metrics(self) -> Dict[str, Any]:
        risk_engine = PredictiveRiskEngine(self.state, num_simulations=1000)
        risk = risk_engine.analyze_risk()
        return {
            "predicted_finish": float(self.state.target_deadline_days) + risk.predicted_delay_days,
            "cost": float(self.state.budget_spent),
            "prob_delay": risk.probability_of_delay
        }

    def simulate_developer_absence(self, dev_id: str, absent_days: int) -> ScenarioResult:
        """Simulates the impact of a developer being unavailable for absent_days."""
        sim_state = copy.deepcopy(self.state)
        dev = sim_state.developers.get(dev_id)
        dev_name = dev.name if dev else f"Dev #{dev_id}"

        baseline = self._get_baseline_metrics()

        affected_task_keys = []
        # Delay all active/in-progress tasks assigned to this dev
        for task in sim_state.tasks.values():
            if task.assignee_id == dev_id and task.status != TaskStatus.DONE:
                task.remaining_days += float(absent_days)
                affected_task_keys.append(task.key)

        sim_risk = PredictiveRiskEngine(sim_state, num_simulations=1000).analyze_risk()
        sim_finish = float(sim_state.target_deadline_days) + sim_risk.predicted_delay_days
        delay_delta = round(max(0.0, sim_finish - baseline["predicted_finish"]), 1)

        # Budget impact: cost of delay + burn rate
        daily_team_burn = sum(d.daily_rate for d in self.state.developers.values())
        cost_delta = round(delay_delta * daily_team_burn * 0.75, 2)
        sim_cost = baseline["cost"] + cost_delta

        # Find backup candidate
        underloaded = [d for d in self.state.developers.values() if d.id != dev_id and d.workload_percentage < 75]
        backup_name = underloaded[0].name if underloaded else "External Contractor"

        rec = f"Temporarily reassign {len(affected_task_keys)} tasks from {dev_name} to {backup_name} to prevent +{delay_delta}d slippage."

        return ScenarioResult(
            scenario_id=f"dev_absence_{dev_id}",
            name=f"Developer Unavailable ({dev_name} absent for {absent_days} days)",
            description=f"Simulates {dev_name}'s absence during critical sprint window.",
            baseline_completion_day=baseline["predicted_finish"],
            simulated_completion_day=sim_finish,
            delay_delta_days=delay_delta,
            baseline_cost=baseline["cost"],
            simulated_cost=sim_cost,
            cost_delta=cost_delta,
            affected_tasks=affected_task_keys,
            affected_milestones=["Milestone: Core API Ready", "Milestone: End-to-End Integration Testing"] if delay_delta > 3 else ["Milestone: Core API Ready"],
            recommendation=rec,
            risk_direction="INCREASED" if delay_delta > 0 else "NEUTRAL"
        )

    def simulate_deadline_adjustment(self, shift_days: int) -> ScenarioResult:
        """Simulates shifting the target deadline earlier (-) or later (+)."""
        sim_state = copy.deepcopy(self.state)
        sim_state.target_deadline_days += shift_days

        baseline = self._get_baseline_metrics()
        sim_risk = PredictiveRiskEngine(sim_state, num_simulations=1000).analyze_risk()
        
        sim_finish = float(sim_state.target_deadline_days) + sim_risk.predicted_delay_days
        delay_delta = round(sim_risk.predicted_delay_days, 1)
        
        cost_delta = 0.0 if shift_days > 0 else -15000.0
        sim_cost = baseline["cost"] + cost_delta

        if shift_days > 0:
            rec = f"Extending deadline by {shift_days} days reduces delay probability from {baseline['prob_delay']}% → {sim_risk.probability_of_delay}%."
            risk_dir = "DECREASED"
        else:
            rec = f"Compressing deadline by {abs(shift_days)} days increases deadline breach risk to {sim_risk.probability_of_delay}%."
            risk_dir = "INCREASED"

        return ScenarioResult(
            scenario_id=f"deadline_shift_{shift_days}",
            name=f"Deadline Adjustment ({'+' if shift_days > 0 else ''}{shift_days} days)",
            description=f"Evaluates feasibility of moving project target deadline to Day {sim_state.target_deadline_days}.",
            baseline_completion_day=baseline["predicted_finish"],
            simulated_completion_day=sim_finish,
            delay_delta_days=delay_delta,
            baseline_cost=baseline["cost"],
            simulated_cost=sim_cost,
            cost_delta=cost_delta,
            affected_tasks=[t.key for t in self.state.tasks.values() if t.status != TaskStatus.DONE],
            affected_milestones=["Final Release Gate"],
            recommendation=rec,
            risk_direction=risk_dir
        )

    def simulate_scope_reduction(self, task_ids_to_drop: List[str]) -> ScenarioResult:
        """Simulates deferring or dropping specified tasks to protect release date."""
        sim_state = copy.deepcopy(self.state)
        dropped_keys = []
        saved_points = 0
        saved_cost = 0.0

        for tid in task_ids_to_drop:
            if tid in sim_state.tasks:
                task = sim_state.tasks.pop(tid)
                dropped_keys.append(task.key)
                saved_points += task.story_points
                saved_cost += task.remaining_days * task.daily_burn_cost

        # Remove dependencies pointing to dropped tasks
        for task in sim_state.tasks.values():
            task.dependencies = [d for d in task.dependencies if d not in task_ids_to_drop]

        baseline = self._get_baseline_metrics()
        sim_risk = PredictiveRiskEngine(sim_state, num_simulations=1000).analyze_risk()
        sim_finish = float(sim_state.target_deadline_days) + sim_risk.predicted_delay_days
        delay_delta = round(sim_finish - baseline["predicted_finish"], 1)

        rec = f"Deferring {len(dropped_keys)} non-essential tasks ({', '.join(dropped_keys)}) recovers ~{abs(delay_delta)} days and saves ₹{int(saved_cost):,}."

        return ScenarioResult(
            scenario_id="scope_reduction",
            name=f"Scope Descope ({len(dropped_keys)} tasks removed)",
            description=f"Simulates dropping non-critical items ({', '.join(dropped_keys)}) to hit deadline.",
            baseline_completion_day=baseline["predicted_finish"],
            simulated_completion_day=sim_finish,
            delay_delta_days=delay_delta,
            baseline_cost=baseline["cost"],
            simulated_cost=max(0.0, baseline["cost"] - saved_cost),
            cost_delta=-saved_cost,
            affected_tasks=dropped_keys,
            affected_milestones=["Scope Baseline v2.0"],
            recommendation=rec,
            risk_direction="DECREASED"
        )
