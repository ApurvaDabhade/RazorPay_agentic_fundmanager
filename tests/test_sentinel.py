"""
Unit tests for Project Sentinel
"""

import unittest
from sentinel.models import (
    ProjectState,
    Task,
    Developer,
    TaskStatus,
    TaskPriority,
    HealthTier,
    ActionStatus
)
from sentinel.sample_data import get_razorpay_project_state, get_ecommerce_project_state
from sentinel.dependency_engine import DependencyEngine
from sentinel.predictive_engine import PredictiveRiskEngine
from sentinel.health_engine import HealthScoreEngine
from sentinel.root_cause_engine import RootCauseInvestigator
from sentinel.resource_optimizer import ResourceOptimizer
from sentinel.scenario_simulator import ScenarioSimulator
from sentinel.project_memory import ProjectMemoryStore
from sentinel.action_agent import ActionAgent
from sentinel.orchestrator import SentinelOrchestrator


class TestProjectSentinel(unittest.TestCase):

    def setUp(self):
        self.state = get_razorpay_project_state()

    def test_dependency_engine_cpm_and_dag(self):
        engine = DependencyEngine(self.state)
        self.assertTrue(engine.is_dag())
        critical_path, duration, metrics = engine.compute_critical_path()
        self.assertGreater(len(critical_path), 0)
        self.assertGreater(duration, 0.0)
        self.assertIn("task-3", critical_path)

        # Test Cascade Impact
        cascade = engine.calculate_cascade_impact("task-3", delay_days=3.0)
        self.assertGreater(cascade["affected_downstream_count"], 0)
        self.assertTrue(cascade["is_critical_task"])

    def test_predictive_risk_monte_carlo(self):
        engine = PredictiveRiskEngine(self.state, num_simulations=500)
        risk = engine.analyze_risk()
        self.assertIn(risk.deadline_risk_level, ["HIGH", "MEDIUM", "LOW"])
        self.assertGreaterEqual(risk.probability_of_delay, 0.0)
        self.assertLessEqual(risk.probability_of_delay, 100.0)
        self.assertGreater(len(risk.primary_causes), 0)
        self.assertIsNotNone(risk.confidence_interval_95)

    def test_health_score_engine(self):
        engine = HealthScoreEngine(self.state)
        health = engine.calculate_health()
        self.assertGreaterEqual(health.overall_score, 0)
        self.assertLessEqual(health.overall_score, 100)
        self.assertIn(health.tier, [HealthTier.HEALTHY, HealthTier.NEEDS_ATTENTION, HealthTier.CRITICAL])
        self.assertGreater(len(health.alerts) + len(health.highlights), 0)

    def test_root_cause_investigator(self):
        investigator = RootCauseInvestigator(self.state)
        report = investigator.investigate()
        self.assertGreaterEqual(len(report.chain), 3)
        self.assertTrue(any(node.node_type == "ROOT_CAUSE" for node in report.chain))
        self.assertIn("Rahul", report.root_cause_statement)
        self.assertGreater(len(report.recommended_intervention), 10)

    def test_resource_optimizer(self):
        optimizer = ResourceOptimizer(self.state)
        summary = optimizer.get_team_workload_summary()
        self.assertEqual(len(summary), len(self.state.developers))
        
        # Check Rahul is overloaded
        rahul_entry = next(d for d in summary if "Rahul" in d["name"])
        self.assertGreater(rahul_entry["workload_pct"], 100.0)
        self.assertGreater(rahul_entry["burnout_score"], 60.0)

        # Check rebalancing recommendations
        recs = optimizer.generate_rebalancing_recommendations()
        self.assertGreater(len(recs), 0)
        self.assertEqual(recs[0]["from_dev_id"], "dev-1")
        self.assertEqual(recs[0]["to_dev_id"], "dev-2")

    def test_scenario_simulator(self):
        sim = ScenarioSimulator(self.state)
        # Test developer absence
        res_absence = sim.simulate_developer_absence("dev-1", absent_days=5)
        self.assertGreater(res_absence.delay_delta_days, 0.0)
        self.assertGreater(len(res_absence.affected_tasks), 0)

        # Test deadline shift
        res_shift = sim.simulate_deadline_adjustment(shift_days=3)
        self.assertIsNotNone(res_shift.recommendation)

        # Test scope reduction
        res_scope = sim.simulate_scope_reduction(["task-5"])
        self.assertIn("PAY-105", res_scope.affected_tasks)

    def test_project_memory_store(self):
        memory = ProjectMemoryStore()
        # Query existing memories
        results = memory.query("Razorpay webhook")
        self.assertGreater(len(results), 0)

        # Q&A test
        qa = memory.answer_question("Why did we select Razorpay?")
        self.assertIn("Razorpay", qa["answer"])

        # Add memory
        entry = memory.add_entry(
            category="DECISION",
            title="Adopted Project Sentinel",
            content="Team adopted Project Sentinel for autonomous predictive project management.",
            tags=["sentinel", "ai"]
        )
        self.assertEqual(entry.title, "Adopted Project Sentinel")

    def test_action_agent_hitl_lifecycle(self):
        agent = ActionAgent(self.state)
        pending = agent.get_pending_actions()
        self.assertGreater(len(pending), 0)

        action_id = pending[0].action_id
        res = agent.approve_and_execute(action_id)
        self.assertTrue(res["success"])
        self.assertEqual(pending[0].status, ActionStatus.EXECUTED)
        self.assertIsNotNone(pending[0].executed_at)

    def test_sentinel_orchestrator(self):
        orchestrator = SentinelOrchestrator(self.state)
        cycle_result = orchestrator.run_full_cycle()
        self.assertIn("health", cycle_result)
        self.assertIn("risk", cycle_result)
        self.assertIn("root_cause", cycle_result)
        self.assertIn("team_workload", cycle_result)
        self.assertIn("scenarios", cycle_result)


if __name__ == "__main__":
    unittest.main()
