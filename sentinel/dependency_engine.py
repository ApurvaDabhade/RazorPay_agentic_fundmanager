"""
sentinel.dependency_engine
Dependency Intelligence DAG, Critical Path Method (CPM), and Cascade Risk Propagation
Pure Python Standard Library implementation with zero external dependencies.
"""

from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict, deque
from .models import ProjectState, Task, TaskStatus


class DependencyEngine:
    """Analyzes task dependencies, computes critical paths, and models risk propagation."""

    def __init__(self, state: ProjectState):
        self.state = state
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.predecessors: Dict[str, List[str]] = defaultdict(list)
        self.successors: Dict[str, List[str]] = defaultdict(list)
        self._build_graph()

    def _build_graph(self):
        """Constructs adjacency graph from project tasks."""
        self.nodes.clear()
        self.predecessors.clear()
        self.successors.clear()

        for task_id, task in self.state.tasks.items():
            self.nodes[task_id] = {
                "key": task.key,
                "title": task.title,
                "duration": max(0.1, task.remaining_days),
                "status": task.status.value,
                "assignee": task.assignee_id,
                "story_points": task.story_points,
                "is_blocked": (task.status == TaskStatus.BLOCKED)
            }
            # Ensure keys exist in adjacency dicts
            _ = self.predecessors[task_id]
            _ = self.successors[task_id]

        for task_id, task in self.state.tasks.items():
            for dep_id in task.dependencies:
                if dep_id in self.state.tasks:
                    # dep_id must complete before task_id can start
                    self.predecessors[task_id].append(dep_id)
                    self.successors[dep_id].append(task_id)

    def is_dag(self) -> bool:
        """Returns True if the dependency structure has no cyclic deadlocks (using Kahn's algorithm)."""
        in_degree = {u: len(self.predecessors[u]) for u in self.nodes}
        queue = deque([u for u, deg in in_degree.items() if deg == 0])
        visited_count = 0

        while queue:
            node = queue.popleft()
            visited_count += 1
            for succ in self.successors[node]:
                in_degree[succ] -= 1
                if in_degree[succ] == 0:
                    queue.append(succ)

        return visited_count == len(self.nodes)

    def get_topological_order(self) -> List[str]:
        """Returns tasks in valid topological execution order."""
        in_degree = {u: len(self.predecessors[u]) for u in self.nodes}
        queue = deque([u for u, deg in in_degree.items() if deg == 0])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for succ in self.successors[node]:
                in_degree[succ] -= 1
                if in_degree[succ] == 0:
                    queue.append(succ)

        if len(order) < len(self.nodes):
            # If cycle, append remaining nodes to prevent crashes
            for u in self.nodes:
                if u not in order:
                    order.append(u)

        return order

    def compute_critical_path(self) -> Tuple[List[str], float, Dict[str, Dict[str, float]]]:
        """
        Computes Critical Path using CPM (Early Start/Finish & Late Start/Finish).
        Returns (critical_path_task_ids, total_project_duration, task_schedule_metrics).
        """
        if not self.nodes:
            return [], 0.0, {}

        topo_order = self.get_topological_order()
        es: Dict[str, float] = {}  # Early Start
        ef: Dict[str, float] = {}  # Early Finish

        # Forward Pass
        for node in topo_order:
            preds = self.predecessors.get(node, [])
            pred_efs = [ef[p] for p in preds if p in ef]
            es[node] = max(pred_efs) if pred_efs else 0.0
            duration = self.nodes[node]["duration"]
            ef[node] = es[node] + duration

        max_duration = max(ef.values()) if ef else 0.0

        # Backward Pass
        ls: Dict[str, float] = {}  # Late Start
        lf: Dict[str, float] = {}  # Late Finish

        for node in reversed(topo_order):
            succs = self.successors.get(node, [])
            succ_lss = [ls[s] for s in succs if s in ls]
            lf[node] = min(succ_lss) if succ_lss else max_duration
            duration = self.nodes[node]["duration"]
            ls[node] = lf[node] - duration

        metrics: Dict[str, Dict[str, float]] = {}
        critical_path: List[str] = []

        for node in topo_order:
            slack = ls[node] - es[node]
            is_critical = abs(slack) < 1e-4
            if is_critical:
                critical_path.append(node)
            metrics[node] = {
                "ES": round(es[node], 2),
                "EF": round(ef[node], 2),
                "LS": round(ls[node], 2),
                "LF": round(lf[node], 2),
                "slack": round(max(0.0, slack), 2),
                "is_critical": is_critical
            }

        return critical_path, round(max_duration, 2), metrics

    def _get_descendants(self, start_node: str) -> Set[str]:
        """BFS to collect all downstream reachable tasks."""
        descendants: Set[str] = set()
        queue = deque([start_node])
        while queue:
            curr = queue.popleft()
            for succ in self.successors.get(curr, []):
                if succ not in descendants:
                    descendants.add(succ)
                    queue.append(succ)
        return descendants

    def calculate_cascade_impact(self, delayed_task_id: str, delay_days: float) -> Dict[str, Any]:
        """
        Calculates how a delay on delayed_task_id cascades through downstream tasks.
        """
        if delayed_task_id not in self.nodes:
            return {"affected_tasks": [], "project_delay_delta": 0.0, "affected_count": 0}

        downstream_nodes = list(self._get_descendants(delayed_task_id))
        critical_path, baseline_duration, _ = self.compute_critical_path()

        # Simulate impact with delayed task duration
        orig_duration = self.nodes[delayed_task_id]["duration"]
        self.nodes[delayed_task_id]["duration"] = orig_duration + delay_days
        _, new_duration, _ = self.compute_critical_path()
        # Revert
        self.nodes[delayed_task_id]["duration"] = orig_duration

        project_delay_delta = max(0.0, new_duration - baseline_duration)

        affected_details = []
        for d_id in downstream_nodes:
            task = self.state.tasks.get(d_id)
            if task:
                affected_details.append({
                    "task_id": d_id,
                    "key": task.key,
                    "title": task.title,
                    "assignee": task.assignee_id,
                    "status": task.status.value,
                    "is_on_critical_path": d_id in critical_path
                })

        return {
            "delayed_task_id": delayed_task_id,
            "delayed_task_key": self.state.tasks[delayed_task_id].key,
            "delay_days": delay_days,
            "affected_downstream_count": len(downstream_nodes),
            "affected_tasks": affected_details,
            "project_delay_delta": round(project_delay_delta, 2),
            "is_critical_task": delayed_task_id in critical_path
        }

    def get_dependency_tree_summary(self) -> List[Dict[str, Any]]:
        """Returns structured hierarchy summary for UI visualization."""
        summary = []
        critical_path, _, metrics = self.compute_critical_path()

        for task_id, task in self.state.tasks.items():
            deps = [self.state.tasks[d].key for d in task.dependencies if d in self.state.tasks]
            downstream = [self.state.tasks[d].key for d in self.successors.get(task_id, []) if d in self.state.tasks]
            m = metrics.get(task_id, {})
            summary.append({
                "id": task_id,
                "key": task.key,
                "title": task.title,
                "assignee": task.assignee_id,
                "status": task.status.value,
                "dependencies": deps,
                "downstream": downstream,
                "is_critical": task_id in critical_path,
                "slack": m.get("slack", 0.0),
                "ES": m.get("ES", 0.0),
                "EF": m.get("EF", 0.0),
            })
        return summary
