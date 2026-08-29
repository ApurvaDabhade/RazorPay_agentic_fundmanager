"""
sentinel.health_engine
Dynamic Multi-Dimensional Project Health Scoring Engine (0-100)
"""

from typing import List
from .models import ProjectState, HealthBreakdown, HealthTier, TaskStatus
from .predictive_engine import PredictiveRiskEngine
from .dependency_engine import DependencyEngine


class HealthScoreEngine:
    """Computes a multi-dimensional, dynamic Project Health Score (0-100)."""

    def __init__(self, state: ProjectState):
        self.state = state
        self.risk_engine = PredictiveRiskEngine(state, num_simulations=1000)
        self.dep_engine = DependencyEngine(state)

    def calculate_health(self) -> HealthBreakdown:
        risk = self.risk_engine.analyze_risk()
        critical_path, _, metrics = self.dep_engine.compute_critical_path()

        # 1. Schedule Score (Weight: 25%)
        # Based on progress gap and predicted delay
        progress_gap = max(0.0, risk.expected_progress_pct - risk.current_progress_pct)
        schedule_score = max(10, int(100 - (progress_gap * 1.8) - (risk.predicted_delay_days * 5)))
        schedule_score = min(100, max(0, schedule_score))

        # 2. Budget Score (Weight: 15%)
        # Expected spend = (current_day / target_deadline) * total_budget
        expected_spend = (self.state.current_day / max(1, self.state.target_deadline_days)) * self.state.budget_allocated
        if expected_spend > 0:
            budget_variance_pct = ((self.state.budget_spent - expected_spend) / expected_spend) * 100
        else:
            budget_variance_pct = 0.0

        if budget_variance_pct > 20:
            budget_score = max(20, int(100 - (budget_variance_pct * 2)))
        elif budget_variance_pct < -10:
            budget_score = 95
        else:
            budget_score = max(50, int(100 - abs(budget_variance_pct)))
        budget_score = min(100, max(0, budget_score))

        # 3. Resources Score (Weight: 20%)
        # Penalize overloaded (>110%) and severely underutilized (<40%) developers
        overloaded_count = sum(1 for d in self.state.developers.values() if d.workload_percentage > 110)
        avg_burnout = sum(d.burnout_risk_score for d in self.state.developers.values()) / max(1, len(self.state.developers))
        resources_score = int(100 - (overloaded_count * 20) - (avg_burnout * 0.4))
        resources_score = min(100, max(0, resources_score))

        # 4. Dependencies Score (Weight: 15%)
        blocked_tasks = sum(1 for t in self.state.tasks.values() if t.status == TaskStatus.BLOCKED)
        blocked_on_cp = sum(1 for cp_id in critical_path if self.state.tasks.get(cp_id) and self.state.tasks[cp_id].status == TaskStatus.BLOCKED)
        dependencies_score = int(100 - (blocked_tasks * 12) - (blocked_on_cp * 25))
        dependencies_score = min(100, max(0, dependencies_score))

        # 5. Risk Score (Weight: 15%)
        # Inverse of probability of delay
        risk_score = int(max(0, 100 - (risk.probability_of_delay * 0.85)))
        risk_score = min(100, max(0, risk_score))

        # 6. Quality Score (Weight: 10%)
        # Based on review bottlenecks and task completion rates
        review_tasks = sum(1 for t in self.state.tasks.values() if t.status == TaskStatus.REVIEW)
        quality_score = max(30, int(95 - (review_tasks * 8)))

        # Weighted Overall Score
        overall = int(
            (schedule_score * 0.25) +
            (budget_score * 0.15) +
            (resources_score * 0.20) +
            (dependencies_score * 0.15) +
            (risk_score * 0.15) +
            (quality_score * 0.10)
        )
        overall = min(100, max(0, overall))

        # Determine Tier
        if overall >= 80:
            tier = HealthTier.HEALTHY
        elif overall >= 60:
            tier = HealthTier.NEEDS_ATTENTION
        else:
            tier = HealthTier.CRITICAL

        # Generate Highlights and Alerts
        highlights = []
        alerts = []

        if schedule_score >= 80:
            highlights.append("Schedule tracking close to sprint baseline.")
        else:
            alerts.append(f"Schedule slippage predicted: +{risk.predicted_delay_days} days delay probability {risk.probability_of_delay}%.")

        if resources_score < 70:
            alerts.append(f"{overloaded_count} developer(s) exceed safe capacity threshold (>110%).")
        else:
            highlights.append("Team resource allocation balanced across workstreams.")

        if blocked_tasks > 0:
            alerts.append(f"{blocked_tasks} task(s) currently blocked ({blocked_on_cp} directly on critical path).")
        else:
            highlights.append("Zero blocked tasks detected in active sprint.")

        return HealthBreakdown(
            overall_score=overall,
            schedule_score=schedule_score,
            budget_score=budget_score,
            resources_score=resources_score,
            dependencies_score=dependencies_score,
            risk_score=risk_score,
            quality_score=quality_score,
            tier=tier,
            highlights=highlights,
            alerts=alerts
        )
