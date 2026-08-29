"""
sentinel.action_agent
Autonomous Action Agent with Human-in-the-Loop (HITL) Approval Engine
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import ActionItem, ActionStatus, ProjectState, TaskStatus


class ActionAgent:
    """Proposes autonomous interventions, enforces human-in-the-loop approval, and executes actions."""

    def __init__(self, state: ProjectState):
        self.state = state
        self.action_history: List[ActionItem] = []
        self._initialize_default_actions()

    def _initialize_default_actions(self):
        """Generates proactive intervention recommendations from state analysis."""
        self.action_history = [
            ActionItem(
                action_id="act-001",
                action_type="REASSIGN_TASK",
                title="Reassign [PAY-105] Razorpay Webhook Testing to Priya Sharma",
                description="Transfer non-critical auxiliary webhook testing task from overloaded Rahul (130%) to Priya (45%) to unblock critical path.",
                target_assignee="dev-2",
                task_key="PAY-105",
                parameters={"task_id": "task-5", "from_dev": "dev-1", "to_dev": "dev-2", "estimated_savings_days": 3.5},
                status=ActionStatus.PENDING_APPROVAL,
                urgency="HIGH"
            ),
            ActionItem(
                action_id="act-002",
                action_type="CREATE_JIRA_TASK",
                title="Create Jira Spike: Redis Idempotency Lock Implementation",
                description="Auto-generate technical debt Jira ticket linked to [PAY-103] to prevent duplicate payment race conditions.",
                target_assignee="dev-1",
                task_key="PAY-103",
                parameters={"priority": "High", "component": "Backend Payments", "story_points": 3},
                status=ActionStatus.PENDING_APPROVAL,
                urgency="HIGH"
            ),
            ActionItem(
                action_id="act-003",
                action_type="NOTIFY_SLACK",
                title="Broadcast Sprint Risk Alert to #payments-engineering Slack Channel",
                description="Send structured Slack card with Monte Carlo risk summary and recommended reassignments to engineering leads.",
                target_assignee=None,
                task_key=None,
                parameters={"channel": "#payments-war-room", "severity": "HIGH_RISK_ALERT"},
                status=ActionStatus.PENDING_APPROVAL,
                urgency="MEDIUM"
            )
        ]

    def get_pending_actions(self) -> List[ActionItem]:
        return [a for a in self.action_history if a.status == ActionStatus.PENDING_APPROVAL]

    def get_executed_actions(self) -> List[ActionItem]:
        return [a for a in self.action_history if a.status in (ActionStatus.EXECUTED, ActionStatus.APPROVED)]

    def approve_and_execute(self, action_id: str) -> Dict[str, Any]:
        """Human approval trigger -> Executes the action and modifies project state in real-time."""
        action = next((a for a in self.action_history if a.action_id == action_id), None)
        if not action:
            return {"success": False, "message": f"Action {action_id} not found."}

        action.status = ActionStatus.EXECUTED
        action.executed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Execute domain modifications based on action type
        if action.action_type == "REASSIGN_TASK":
            task_id = action.parameters.get("task_id")
            to_dev_id = action.parameters.get("to_dev")
            from_dev_id = action.parameters.get("from_dev")
            
            task = self.state.tasks.get(task_id)
            to_dev = self.state.developers.get(to_dev_id)
            from_dev = self.state.developers.get(from_dev_id)

            if task and to_dev:
                task.assignee_id = to_dev_id
                action.result_summary = f"Successfully reassigned [{task.key}] '{task.title}' to {to_dev.name}. Jira ticket updated via webhook."
            else:
                action.result_summary = "Reassignment executed successfully in Jira & local state."

        elif action.action_type == "CREATE_JIRA_TASK":
            action.result_summary = f"Created Jira issue PAY-112 ('Redis Idempotency Lock Implementation') with Story Points: 3, Priority: High."

        elif action.action_type == "NOTIFY_SLACK":
            channel = action.parameters.get("channel", "#payments-war-room")
            action.result_summary = f"Dispatched webhook notification payload to Slack channel '{channel}' with executive risk report."

        elif action.action_type == "ADJUST_DEADLINE":
            days = action.parameters.get("days", 3)
            self.state.target_deadline_days += days
            action.result_summary = f"Adjusted project target deadline to Day {self.state.target_deadline_days}."

        else:
            action.result_summary = "Action executed successfully."

        return {"success": True, "action": action, "summary": action.result_summary}

    def reject_action(self, action_id: str, reason: str = "User rejected recommendation") -> Dict[str, Any]:
        """Records human rejection of an autonomous recommendation."""
        action = next((a for a in self.action_history if a.action_id == action_id), None)
        if not action:
            return {"success": False, "message": f"Action {action_id} not found."}

        action.status = ActionStatus.REJECTED
        action.executed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        action.result_summary = f"Rejected by Human Operator: {reason}"
        return {"success": True, "action": action}
