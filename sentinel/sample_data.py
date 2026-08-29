"""
sentinel.sample_data
Pre-configured realistic project datasets for hackathon demonstrations
"""

from typing import Dict
from .models import ProjectState, Task, TaskStatus, TaskPriority, Developer


def get_razorpay_project_state() -> ProjectState:
    """Returns the flagship Razorpay Payment Gateway Integration project state."""
    tasks: Dict[str, Task] = {
        "task-1": Task(
            id="task-1",
            key="PAY-101",
            title="Razorpay Merchant Account & API Key Setup",
            description="Provision test & live keys, configure IP whitelist and webhook signing secrets.",
            assignee_id="dev-3",
            estimated_days=2.0,
            remaining_days=0.0,
            actual_days_spent=2.0,
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            dependencies=[],
            completion_percentage=100.0,
            story_points=2,
            tags=["backend", "security", "razorpay"]
        ),
        "task-2": Task(
            id="task-2",
            key="PAY-102",
            title="Checkout UI Modal & Custom Theme Integration",
            description="Embed Razorpay Standard Checkout SDK into React frontend with responsive mobile styling.",
            assignee_id="dev-4",
            estimated_days=4.0,
            remaining_days=0.0,
            actual_days_spent=4.0,
            status=TaskStatus.DONE,
            priority=TaskPriority.MEDIUM,
            dependencies=["task-1"],
            completion_percentage=100.0,
            story_points=5,
            tags=["frontend", "react", "ui"]
        ),
        "task-3": Task(
            id="task-3",
            key="PAY-103",
            title="Backend Webhook Signature Verification & Idempotency Engine",
            description="Implement HMAC-SHA256 signature verification and Redis idempotency lock for payment.captured events.",
            assignee_id="dev-1",
            estimated_days=5.0,
            remaining_days=3.5,
            actual_days_spent=4.5,
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.CRITICAL,
            dependencies=["task-1"],
            completion_percentage=45.0,
            story_points=8,
            tags=["backend", "razorpay", "security", "redis"],
            blocker_reason="Redis cluster distributed lock specs pending review; engineer handling multiple parallel tickets."
        ),
        "task-4": Task(
            id="task-4",
            key="PAY-104",
            title="UPI AutoPay Mandate & Recurring Billing Service",
            description="Handle recurring subscription authorization and mandate registration webhooks via Razorpay Subscriptions API.",
            assignee_id="dev-1",
            estimated_days=4.0,
            remaining_days=4.0,
            actual_days_spent=0.0,
            status=TaskStatus.BLOCKED,
            priority=TaskPriority.HIGH,
            dependencies=["task-3"],
            completion_percentage=0.0,
            story_points=8,
            tags=["backend", "upi", "subscriptions"],
            blocker_reason="Strictly blocked on PAY-103 Webhook verification engine completion."
        ),
        "task-5": Task(
            id="task-5",
            key="PAY-105",
            title="Webhook Mock Load Testing & Chaos Replay Suite",
            description="Create automated test harness to simulate out-of-order webhooks, network latency, and retry floods.",
            assignee_id="dev-1",
            estimated_days=3.0,
            remaining_days=2.5,
            actual_days_spent=1.0,
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.MEDIUM,
            dependencies=["task-3"],
            completion_percentage=20.0,
            story_points=5,
            tags=["testing", "qa", "chaos", "python"],
            blocker_reason="Currently starved of developer bandwidth."
        ),
        "task-6": Task(
            id="task-6",
            key="PAY-106",
            title="Automated Refund & Settlement Reconciliation Worker",
            description="Daily cron job reconciling bank settlements vs Razorpay ledger and processing instant refunds.",
            assignee_id="dev-2",
            estimated_days=4.0,
            remaining_days=4.0,
            actual_days_spent=0.0,
            status=TaskStatus.TODO,
            priority=TaskPriority.HIGH,
            dependencies=["task-4"],
            completion_percentage=0.0,
            story_points=5,
            tags=["backend", "finance", "reconciliation", "python"]
        ),
        "task-7": Task(
            id="task-7",
            key="PAY-107",
            title="PCI-DSS Security Compliance & Tokenization Audit",
            description="Verify zero raw card data is logged or stored; validate TLS 1.3 encryption and audit trails.",
            assignee_id="dev-3",
            estimated_days=3.0,
            remaining_days=2.0,
            actual_days_spent=1.0,
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            dependencies=["task-1"],
            completion_percentage=35.0,
            story_points=3,
            tags=["security", "compliance", "audit"]
        ),
        "task-8": Task(
            id="task-8",
            key="PAY-108",
            title="Production Canary Rollout & Observability Dashboard",
            description="Deploy Canary to 5% live merchant traffic; configure CloudWatch alerts for payment drop-offs.",
            assignee_id="dev-3",
            estimated_days=3.0,
            remaining_days=3.0,
            actual_days_spent=0.0,
            status=TaskStatus.TODO,
            priority=TaskPriority.CRITICAL,
            dependencies=["task-6", "task-7"],
            completion_percentage=0.0,
            story_points=4,
            tags=["devops", "deployment", "monitoring"]
        )
    }

    developers: Dict[str, Developer] = {
        "dev-1": Developer(
            id="dev-1",
            name="Rahul Verma",
            role="Lead Backend Engineer",
            capacity_points_per_sprint=16.0,
            assigned_points=21.0,
            workload_percentage=131.2,
            assigned_task_ids=["task-3", "task-4", "task-5"],
            skills=["backend", "razorpay", "security", "redis", "upi", "python"],
            daily_rate=7500.0,
            burnout_risk_score=88.5
        ),
        "dev-2": Developer(
            id="dev-2",
            name="Priya Sharma",
            role="Fullstack & QA Engineer",
            capacity_points_per_sprint=18.0,
            assigned_points=5.0,
            workload_percentage=27.7,
            assigned_task_ids=["task-6"],
            skills=["backend", "testing", "qa", "chaos", "reconciliation", "python"],
            daily_rate=6000.0,
            burnout_risk_score=20.0
        ),
        "dev-3": Developer(
            id="dev-3",
            name="Amit Patel",
            role="DevOps & Security Specialist",
            capacity_points_per_sprint=15.0,
            assigned_points=7.0,
            workload_percentage=46.6,
            assigned_task_ids=["task-1", "task-7", "task-8"],
            skills=["devops", "security", "compliance", "deployment", "monitoring"],
            daily_rate=6500.0,
            burnout_risk_score=40.0
        ),
        "dev-4": Developer(
            id="dev-4",
            name="Sneha Roy",
            role="Senior Frontend Engineer",
            capacity_points_per_sprint=16.0,
            assigned_points=0.0,
            workload_percentage=0.0,
            assigned_task_ids=["task-2"],
            skills=["frontend", "react", "ui", "javascript"],
            daily_rate=6200.0,
            burnout_risk_score=25.0
        )
    }

    return ProjectState(
        project_id="proj-razorpay-v1",
        name="Razorpay Payment Gateway Core Integration",
        description="High-security payment processing service supporting UPI AutoPay, cards, and automated instant reconciliation.",
        target_deadline_days=18,
        current_day=11,
        budget_allocated=350000.0,
        budget_spent=245000.0,
        tasks=tasks,
        developers=developers,
        historical_velocity_avg=3.2,
        historical_velocity_std=0.75
    )


def get_ecommerce_project_state() -> ProjectState:
    """Returns an E-Commerce Flash Sale Scaling project state."""
    tasks: Dict[str, Task] = {
        "e-1": Task(
            id="e-1",
            key="ECOMM-201",
            title="Database Read Replica & Connection Pool Optimization",
            description="Configure PgBouncer and Postgres read replicas for 10x traffic spike.",
            assignee_id="d-1",
            estimated_days=3.0,
            remaining_days=0.0,
            actual_days_spent=3.0,
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            dependencies=[],
            completion_percentage=100.0,
            story_points=3
        ),
        "e-2": Task(
            id="e-2",
            key="ECOMM-202",
            title="Distributed Inventory Locking Service",
            description="Prevent race-condition overselling using Redis Redlock.",
            assignee_id="d-1",
            estimated_days=5.0,
            remaining_days=2.5,
            actual_days_spent=4.0,
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.CRITICAL,
            dependencies=["e-1"],
            completion_percentage=60.0,
            story_points=16,
            blocker_reason="High lock contention under stress testing."
        ),
        "e-3": Task(
            id="e-3",
            key="ECOMM-203",
            title="Cart Checkout One-Click Flow",
            description="Streamline mobile checkout funnel from 4 steps down to 1 step.",
            assignee_id="d-2",
            estimated_days=4.0,
            remaining_days=3.0,
            actual_days_spent=1.0,
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            dependencies=["e-2"],
            completion_percentage=25.0,
            story_points=5
        )
    }

    developers: Dict[str, Developer] = {
        "d-1": Developer(
            id="d-1",
            name="Vikram Singh",
            role="Senior Systems Architect",
            capacity_points_per_sprint=15.0,
            assigned_points=16.0,
            workload_percentage=106.7,
            assigned_task_ids=["e-1", "e-2"],
            burnout_risk_score=72.0
        ),
        "d-2": Developer(
            id="d-2",
            name="Ananya Sen",
            role="Frontend Lead",
            capacity_points_per_sprint=18.0,
            assigned_points=5.0,
            workload_percentage=27.7,
            assigned_task_ids=["e-3"],
            burnout_risk_score=30.0
        )
    }

    return ProjectState(
        project_id="proj-ecomm-scaling",
        name="Flash Sale Scalability & One-Click Checkout",
        description="Infrastructure and UI overhaul to handle Black Friday traffic peaks without cart drop-offs.",
        target_deadline_days=14,
        current_day=8,
        budget_allocated=280000.0,
        budget_spent=160000.0,
        tasks=tasks,
        developers=developers,
        historical_velocity_avg=3.0,
        historical_velocity_std=0.6
    )
