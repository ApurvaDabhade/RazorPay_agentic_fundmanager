"""
sentinel.resource_optimizer
Team Workload Analytics, Burnout Risk Modeling, and AI Resource Optimization
Pure Python Standard Library implementation with zero external dependencies.
"""

from typing import Dict, List, Any
from .models import ProjectState, Developer, Task, TaskStatus


class ResourceOptimizer:
    """Analyzes team bandwidth, detects burnout risks, and computes optimal task rebalancing."""

    def __init__(self, state: ProjectState):
        self.state = state
        self._recalculate_workloads()

    def _recalculate_workloads(self):
        """Refreshes workload points, percentages, and burnout risk scores."""
        for dev in self.state.developers.values():
            # Sum remaining points assigned to dev
            assigned_tasks = [
                t for t in self.state.tasks.values() 
                if t.assignee_id == dev.id and t.status != TaskStatus.DONE
            ]
            assigned_points = sum(t.story_points for t in assigned_tasks)
            dev.assigned_points = float(assigned_points)
            dev.assigned_task_ids = [t.id for t in assigned_tasks]
            
            capacity = max(1.0, dev.capacity_points_per_sprint)
            dev.workload_percentage = round((assigned_points / capacity) * 100, 1)

            # Burnout risk model: overload factor + context switching penalty + blocked task stress
            overload_penalty = max(0.0, (dev.workload_percentage - 100.0) * 1.8)
            context_switch_penalty = max(0.0, (len(assigned_tasks) - 3) * 6.0)
            blocked_count = sum(1 for t in assigned_tasks if t.status == TaskStatus.BLOCKED)
            blocked_penalty = blocked_count * 10.0

            raw_burnout = min(100.0, max(5.0, (dev.workload_percentage * 0.4) + overload_penalty + context_switch_penalty + blocked_penalty))
            dev.burnout_risk_score = round(raw_burnout, 1)

    def get_team_workload_summary(self) -> List[Dict[str, Any]]:
        """Returns structured workload and burnout metrics for all developers."""
        self._recalculate_workloads()
        summary = []
        for dev in self.state.developers.values():
            if dev.workload_percentage >= 115:
                status_label = "OVERLOADED ⚠️"
                badge_color = "red"
            elif dev.workload_percentage <= 55:
                status_label = "UNDERUTILIZED 🟢"
                badge_color = "green"
            else:
                status_label = "OPTIMAL ⚖️"
                badge_color = "blue"

            summary.append({
                "id": dev.id,
                "name": dev.name,
                "role": dev.role,
                "workload_pct": dev.workload_percentage,
                "assigned_points": dev.assigned_points,
                "capacity_points": dev.capacity_points_per_sprint,
                "burnout_score": dev.burnout_risk_score,
                "active_task_count": len(dev.assigned_task_ids),
                "skills": dev.skills,
                "status_label": status_label,
                "badge_color": badge_color
            })
        return sorted(summary, key=lambda x: x["workload_pct"], reverse=True)

    def generate_rebalancing_recommendations(self) -> List[Dict[str, Any]]:
        """
        Calculates optimal task rebalancing transfers from overloaded developers to underutilized developers.
        """
        self._recalculate_workloads()
        recommendations = []

        overloaded_devs = [d for d in self.state.developers.values() if d.workload_percentage > 105]
        underloaded_devs = [d for d in self.state.developers.values() if d.workload_percentage < 80]

        if not overloaded_devs or not underloaded_devs:
            return []

        for o_dev in overloaded_devs:
            # Look at candidate tasks to move (prefer non-critical or auxiliary tasks)
            dev_tasks = [
                self.state.tasks[t_id] for t_id in o_dev.assigned_task_ids 
                if t_id in self.state.tasks and self.state.tasks[t_id].status != TaskStatus.DONE
            ]
            dev_tasks.sort(key=lambda t: t.story_points)

            for task in dev_tasks:
                for u_dev in underloaded_devs:
                    has_skill_match = bool(set(task.tags).intersection(set(u_dev.skills))) or len(u_dev.skills) == 0
                    can_take_load = (u_dev.assigned_points + task.story_points) <= (u_dev.capacity_points_per_sprint * 1.05)

                    if has_skill_match and can_take_load:
                        projected_from_workload = round(((o_dev.assigned_points - task.story_points) / max(1, o_dev.capacity_points_per_sprint)) * 100, 1)
                        projected_to_workload = round(((u_dev.assigned_points + task.story_points) / max(1, u_dev.capacity_points_per_sprint)) * 100, 1)

                        recommendations.append({
                            "task_id": task.id,
                            "task_key": task.key,
                            "task_title": task.title,
                            "story_points": task.story_points,
                            "from_dev_id": o_dev.id,
                            "from_dev_name": o_dev.name,
                            "from_current_workload": o_dev.workload_percentage,
                            "from_projected_workload": projected_from_workload,
                            "to_dev_id": u_dev.id,
                            "to_dev_name": u_dev.name,
                            "to_current_workload": u_dev.workload_percentage,
                            "to_projected_workload": projected_to_workload,
                            "reasoning": f"Relieves {o_dev.name}'s workload from {o_dev.workload_percentage}% → {projected_from_workload}% while utilizing {u_dev.name}'s open capacity ({u_dev.workload_percentage}% → {projected_to_workload}%).",
                            "action_prompt": f"Reassign [{task.key}] '{task.title}' from {o_dev.name} to {u_dev.name}"
                        })
                        o_dev.assigned_points -= task.story_points
                        u_dev.assigned_points += task.story_points
                        break

        return recommendations
