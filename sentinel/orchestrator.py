"""
sentinel.orchestrator
Unified Sentinel Multi-Agent Orchestrator
Executes the core cycle: Predict -> Investigate -> Simulate -> Recommend -> Act
"""

from typing import Dict, Any, Optional
from .models import (
    ProjectState,
    HealthBreakdown,
    RiskAssessment,
    RootCauseReport,
    ScenarioResult,
    ActionItem
)
from .dependency_engine import DependencyEngine
from .predictive_engine import PredictiveRiskEngine
from .health_engine import HealthScoreEngine
from .root_cause_engine import RootCauseInvestigator
from .resource_optimizer import ResourceOptimizer
from .scenario_simulator import ScenarioSimulator
from .action_agent import ActionAgent
from .project_memory import ProjectMemoryStore
from .sample_data import get_razorpay_project_state


class SentinelOrchestrator:
    """The central nervous system of Project Sentinel orchestrating predictive intelligence."""

    def __init__(self, state: Optional[ProjectState] = None):
        self.state = state or get_razorpay_project_state()
        self.memory = ProjectMemoryStore()
        self.action_agent = ActionAgent(self.state)

    def set_state(self, state: ProjectState):
        """Updates the active project state and refreshes dependencies."""
        self.state = state
        self.action_agent = ActionAgent(self.state)

    def run_full_cycle(self) -> Dict[str, Any]:
        """
        Executes the autonomous 5-step loop:
        1. Predict (Monte Carlo & Velocity Risk)
        2. Investigate (Root Cause Causal Graph)
        3. Simulate (What-If Perturbations)
        4. Recommend (AI Resource Optimizer & Action Formulations)
        5. Act (Human-in-the-Loop Action Center)
        """
        dep_engine = DependencyEngine(self.state)
        health_engine = HealthScoreEngine(self.state)
        risk_engine = PredictiveRiskEngine(self.state, num_simulations=2000)
        root_cause_engine = RootCauseInvestigator(self.state)
        resource_optimizer = ResourceOptimizer(self.state)
        scenario_simulator = ScenarioSimulator(self.state)

        # 1. Health & Predictive Risk Assessment
        health = health_engine.calculate_health()
        risk = risk_engine.analyze_risk()

        # 2. Dependency Graph & Critical Path
        critical_path, project_duration, metrics = dep_engine.compute_critical_path()
        tree_summary = dep_engine.get_dependency_tree_summary()

        # 3. Root Cause Investigation
        root_cause = root_cause_engine.investigate()

        # 4. Resource Analytics & Rebalancing
        team_workload = resource_optimizer.get_team_workload_summary()
        rebalancing_recommendations = resource_optimizer.generate_rebalancing_recommendations()

        # 5. Default Scenarios Simulation
        # Simulate absence of overloaded dev
        top_dev_id = list(self.state.developers.keys())[0] if self.state.developers else "dev-1"
        scenario_absence = scenario_simulator.simulate_developer_absence(top_dev_id, absent_days=5)
        scenario_shift = scenario_simulator.simulate_deadline_adjustment(shift_days=3)

        # 6. Action Center Items
        pending_actions = self.action_agent.get_pending_actions()
        executed_actions = self.action_agent.get_executed_actions()

        return {
            "project_name": self.state.name,
            "project_description": self.state.description,
            "health": health,
            "risk": risk,
            "critical_path": critical_path,
            "project_duration": project_duration,
            "dependency_tree": tree_summary,
            "root_cause": root_cause,
            "team_workload": team_workload,
            "rebalancing_recommendations": rebalancing_recommendations,
            "scenarios": [scenario_absence, scenario_shift],
            "pending_actions": pending_actions,
            "executed_actions": executed_actions,
            "memory_count": len(self.memory.entries)
        }
