"""
sentinel.models
Data models and schemas for Project Sentinel using standard dataclasses
"""

from enum import Enum
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    REVIEW = "REVIEW"
    DONE = "DONE"


class TaskPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class HealthTier(str, Enum):
    HEALTHY = "HEALTHY"            # 80-100
    NEEDS_ATTENTION = "NEEDS_ATTENTION"  # 60-79
    CRITICAL = "CRITICAL"          # 0-59


@dataclass
class Task:
    id: str
    key: str  # e.g., "PAY-101"
    title: str
    assignee_id: str
    estimated_days: float
    remaining_days: float
    description: str = ""
    actual_days_spent: float = 0.0
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = field(default_factory=list)  # IDs of prerequisite tasks
    completion_percentage: float = 0.0
    story_points: int = 3
    daily_burn_cost: float = 5000.0
    tags: List[str] = field(default_factory=list)
    blocker_reason: Optional[str] = None


@dataclass
class Developer:
    id: str
    name: str
    role: str
    capacity_points_per_sprint: float = 20.0
    assigned_points: float = 0.0
    workload_percentage: float = 0.0
    assigned_task_ids: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    daily_rate: float = 6000.0
    burnout_risk_score: float = 0.0


@dataclass
class ProjectState:
    project_id: str
    name: str
    description: str
    target_deadline_days: int
    current_day: int
    budget_allocated: float
    budget_spent: float
    tasks: Dict[str, Task] = field(default_factory=dict)
    developers: Dict[str, Developer] = field(default_factory=dict)
    historical_velocity_avg: float = 3.5
    historical_velocity_std: float = 0.8


@dataclass
class HealthBreakdown:
    overall_score: int  # 0 - 100
    schedule_score: int
    budget_score: int
    resources_score: int
    dependencies_score: int
    risk_score: int
    quality_score: int
    tier: HealthTier
    highlights: List[str] = field(default_factory=list)
    alerts: List[str] = field(default_factory=list)


@dataclass
class RiskAssessment:
    deadline_risk_level: str  # "HIGH", "MEDIUM", "LOW"
    probability_of_delay: float  # 0 to 100 %
    predicted_delay_days: float
    current_progress_pct: float
    expected_progress_pct: float
    confidence_interval_95: Tuple[float, float]
    primary_causes: List[str] = field(default_factory=list)
    simulation_runs: int = 2000
    trajectory_samples: List[float] = field(default_factory=list)


@dataclass
class RootCauseNode:
    step_number: int
    title: str
    description: str
    node_type: str  # "SYMPTOM", "DEPENDENCY", "BOTTLENECK", "ROOT_CAUSE"
    evidence: str
    severity: str = "HIGH"


@dataclass
class RootCauseReport:
    issue_summary: str
    chain: List[RootCauseNode] = field(default_factory=list)
    root_cause_statement: str = ""
    recommended_intervention: str = ""
    estimated_leverage_impact: str = ""
    confidence_pct: float = 90.0


@dataclass
class ScenarioResult:
    scenario_id: str
    name: str
    description: str
    baseline_completion_day: float
    simulated_completion_day: float
    delay_delta_days: float
    baseline_cost: float
    simulated_cost: float
    cost_delta: float
    affected_tasks: List[str] = field(default_factory=list)
    affected_milestones: List[str] = field(default_factory=list)
    recommendation: str = ""
    risk_direction: str = "NEUTRAL"


class ActionStatus(str, Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    EXECUTED = "EXECUTED"
    REJECTED = "REJECTED"


@dataclass
class ActionItem:
    action_id: str
    action_type: str
    title: str
    description: str
    target_assignee: Optional[str] = None
    task_key: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: ActionStatus = ActionStatus.PENDING_APPROVAL
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    executed_at: Optional[str] = None
    result_summary: Optional[str] = None
    urgency: str = "HIGH"


@dataclass
class MemoryEntry:
    memory_id: str
    category: str
    title: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    tags: List[str] = field(default_factory=list)
    related_tasks: List[str] = field(default_factory=list)
