"""
sentinel.predictive_engine
Monte Carlo Simulation, Velocity Analytics, and Predictive Deadline Risk Detection
Pure Python Standard Library implementation with zero external dependencies.
"""

import random
import math
from typing import Dict, List, Tuple
from .models import ProjectState, RiskAssessment, TaskStatus
from .dependency_engine import DependencyEngine


def _calculate_percentile(data: List[float], percentile: float) -> float:
    """Calculates percentile from sorted list."""
    if not data:
        return 0.0
    k = (len(data) - 1) * (percentile / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return data[int(k)]
    d0 = data[int(f)] * (c - k)
    d1 = data[int(c)] * (k - f)
    return d0 + d1


class PredictiveRiskEngine:
    """Uses stochastic Monte Carlo modeling to predict project delivery risks before they happen."""

    def __init__(self, state: ProjectState, num_simulations: int = 2500):
        self.state = state
        self.num_simulations = num_simulations
        self.dep_engine = DependencyEngine(state)

    def analyze_risk(self) -> RiskAssessment:
        """Runs Monte Carlo simulation and derives deadline risk metrics."""
        critical_path, _, _ = self.dep_engine.compute_critical_path()
        topo_order = self.dep_engine.get_topological_order()

        total_points = sum(t.story_points for t in self.state.tasks.values())
        done_points = sum(t.story_points for t in self.state.tasks.values() if t.status == TaskStatus.DONE)
        in_progress_points = sum(t.story_points * (t.completion_percentage / 100.0)
                                for t in self.state.tasks.values() if t.status in (TaskStatus.IN_PROGRESS, TaskStatus.REVIEW))
        
        current_progress_pct = round(((done_points + in_progress_points) / max(1, total_points)) * 100, 1)
        expected_progress_pct = min(100.0, round((self.state.current_day / max(1, self.state.target_deadline_days)) * 100, 1))

        simulated_finish_days: List[float] = []

        # Monte Carlo Simulation Loop
        for _ in range(self.num_simulations):
            # Sample team velocity factor around historical mean & std
            velocity_sample = max(0.5, random.gauss(
                self.state.historical_velocity_avg,
                self.state.historical_velocity_std
            ))
            velocity_multiplier = self.state.historical_velocity_avg / velocity_sample

            sim_ef: Dict[str, float] = {}

            for node in topo_order:
                task = self.state.tasks.get(node)
                if not task:
                    continue

                pred_finishes = [sim_ef[pred] for pred in self.dep_engine.predecessors.get(node, []) if pred in sim_ef]
                start_time = max(pred_finishes) if pred_finishes else float(self.state.current_day)

                if task.status == TaskStatus.DONE:
                    duration = 0.0
                else:
                    rem_days = max(0.2, task.remaining_days)
                    blocker_mult = 1.6 if task.status == TaskStatus.BLOCKED else 1.0
                    optimistic = rem_days * 0.8
                    most_likely = rem_days * blocker_mult * velocity_multiplier
                    pessimistic = rem_days * 2.2 * blocker_mult * velocity_multiplier

                    # Triangular distribution sampling
                    sample_duration = random.triangular(optimistic, pessimistic, most_likely)
                    duration = max(0.1, sample_duration)

                sim_ef[node] = start_time + duration

            total_sim_duration = max(sim_ef.values()) if sim_ef else float(self.state.current_day)
            simulated_finish_days.append(total_sim_duration)

        simulated_finish_days.sort()
        target = float(self.state.target_deadline_days)

        # Probability of missing target deadline
        missed_count = sum(1 for d in simulated_finish_days if d > target)
        probability_of_delay = round(float((missed_count / self.num_simulations) * 100), 1)

        p50 = _calculate_percentile(simulated_finish_days, 50)
        p90 = _calculate_percentile(simulated_finish_days, 90)
        p5 = _calculate_percentile(simulated_finish_days, 5)
        p95 = _calculate_percentile(simulated_finish_days, 95)

        predicted_delay_days = round(max(0.0, p50 - target), 1)
        if probability_of_delay > 50 and predicted_delay_days == 0.0:
            predicted_delay_days = round(max(0.5, p90 - target), 1)

        # Risk Level Classification
        if probability_of_delay >= 70 or predicted_delay_days >= 5:
            risk_level = "HIGH"
        elif probability_of_delay >= 35 or predicted_delay_days >= 2:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        primary_causes = self._identify_primary_causes(critical_path)

        return RiskAssessment(
            deadline_risk_level=risk_level,
            probability_of_delay=probability_of_delay,
            predicted_delay_days=predicted_delay_days,
            current_progress_pct=current_progress_pct,
            expected_progress_pct=expected_progress_pct,
            confidence_interval_95=(round(p5, 1), round(p95, 1)),
            primary_causes=primary_causes,
            simulation_runs=self.num_simulations,
            trajectory_samples=simulated_finish_days[:100]
        )

    def _identify_primary_causes(self, critical_path: List[str]) -> List[str]:
        """Identifies specific bottlenecks, blocked tasks, and overloaded developers."""
        causes = []

        # 1. Blocked critical path tasks
        for task_id in critical_path:
            task = self.state.tasks.get(task_id)
            if task and task.status == TaskStatus.BLOCKED:
                reason = task.blocker_reason or "Missing prerequisite or external dependency"
                causes.append(f"Blocked on critical path: [{task.key}] {task.title} ({reason})")

        # 2. Overdue or low-progress tasks with high remaining days
        for task_id in critical_path:
            task = self.state.tasks.get(task_id)
            if task and task.status == TaskStatus.IN_PROGRESS and task.completion_percentage < 50 and task.remaining_days > 3:
                causes.append(f"Slow progress on critical path: [{task.key}] {task.title} (Only {task.completion_percentage}% done)")

        # 3. Overloaded assignees on critical path
        for dev_id, dev in self.state.developers.items():
            if dev.workload_percentage > 115:
                causes.append(f"Resource strain: {dev.name} is overloaded at {int(dev.workload_percentage)}% capacity")

        if not causes:
            causes.append("Velocity variance within nominal sprint tolerances.")

        return causes[:4]
