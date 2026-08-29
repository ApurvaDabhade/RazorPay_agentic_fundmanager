"""
sentinel.project_memory
Project Long-Term Memory (Decisions, Incidents, Architecture Trade-offs, Lessons Learned)
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from .models import MemoryEntry


class ProjectMemoryStore:
    """Manages long-term project institutional memory, ADRs, and historical incident retrospectives."""

    def __init__(self, initial_entries: Optional[List[MemoryEntry]] = None):
        self.entries: List[MemoryEntry] = initial_entries or []
        if not self.entries:
            self._load_default_project_memories()

    def _load_default_project_memories(self):
        """Initializes default realistic institutional memory for the project."""
        self.entries = [
            MemoryEntry(
                memory_id="mem-001",
                timestamp="2026-07-15 10:30:00",
                category="ARCHITECTURE",
                title="ADR-01: Microservices vs Monolith for Payment Service",
                content=(
                    "Decided to split the Razorpay Payment Gateway into an isolated microservice with idempotent webhook handlers. "
                    "Rationale: Isolation prevents billing transactions from crashing core app services during traffic surges. "
                    "Trade-off: Requires dedicated webhook signature verification and distributed tracing."
                ),
                tags=["architecture", "razorpay", "microservices", "adr"],
                related_tasks=["PAY-101", "PAY-103"]
            ),
            MemoryEntry(
                memory_id="mem-002",
                timestamp="2026-07-28 14:00:00",
                category="DECISION",
                title="Payment Gateway Provider Selection (Razorpay vs Stripe)",
                content=(
                    "Selected Razorpay as primary payment gateway for domestic UPI & NetBanking processing due to higher success rates (98.4%) and native UPI AutoPay recurring mandate support. "
                    "Stripe maintained as secondary fallback for international card payments."
                ),
                tags=["decision", "razorpay", "payments", "upi"],
                related_tasks=["PAY-101"]
            ),
            MemoryEntry(
                memory_id="mem-003",
                timestamp="2026-08-10 17:45:00",
                category="INCIDENT",
                title="Sprint 2 Post-Mortem: Webhook Timeout Outage",
                content=(
                    "Incident: Razorpay webhook retries caused double balance crediting during load test. "
                    "Root Cause: Webhook handler did not implement Redis distributed locking before DB write. "
                    "Remediation: All payment webhook handlers must enforce Redis idempotency key lock with 60s TTL."
                ),
                tags=["incident", "post-mortem", "webhook", "redis", "idempotency"],
                related_tasks=["PAY-103", "PAY-108"]
            ),
            MemoryEntry(
                memory_id="mem-004",
                timestamp="2026-08-18 11:15:00",
                category="STAKEHOLDER_PREF",
                title="VP of Product Constraint: Zero Downtime Migration",
                content=(
                    "Product leadership explicitly mandated that payment checkout flow cannot have scheduled maintenance downtime. "
                    "Must use blue-green deployments and dual-write database migrations."
                ),
                tags=["stakeholder", "compliance", "uptime", "deployment"],
                related_tasks=["PAY-107"]
            ),
            MemoryEntry(
                memory_id="mem-005",
                timestamp="2026-08-22 09:30:00",
                category="LESSON_LEARNED",
                title="Frontend State Management with Fast Checkout Popups",
                content=(
                    "Lesson: Razorpay Standard Checkout SDK popup event listeners must be cleaned up on React component unmount, "
                    "otherwise orphaned modal callbacks cause memory leaks on mobile Safari."
                ),
                tags=["lesson-learned", "frontend", "react", "safari"],
                related_tasks=["PAY-102"]
            )
        ]

    def add_entry(self, category: str, title: str, content: str, tags: List[str], related_tasks: Optional[List[str]] = None) -> MemoryEntry:
        """Adds a new memory record to the store."""
        entry = MemoryEntry(
            memory_id=f"mem-{len(self.entries) + 1:03d}",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            category=category.upper(),
            title=title,
            content=content,
            tags=tags,
            related_tasks=related_tasks or []
        )
        self.entries.insert(0, entry)
        return entry

    def query(self, search_text: str, category: Optional[str] = None) -> List[MemoryEntry]:
        """Performs contextual search across stored memories."""
        query_words = search_text.lower().split()
        results = []

        for entry in self.entries:
            if category and category != "ALL" and entry.category != category:
                continue

            searchable = f"{entry.title} {entry.content} {' '.join(entry.tags)} {' '.join(entry.related_tasks)}".lower()
            score = sum(1 for word in query_words if word in searchable)
            if score > 0 or not search_text.strip():
                results.append((score, entry))

        # Sort by relevance score descending, then timestamp descending
        results.sort(key=lambda x: (x[0], x[1].timestamp), reverse=True)
        return [r[1] for r in results]

    def answer_question(self, question: str) -> Dict[str, Any]:
        """Provides an intelligent contextual answer to queries regarding past decisions and lessons."""
        relevant_entries = self.query(question)
        if not relevant_entries:
            return {
                "answer": "No historical records or architectural decisions match your query in Project Memory.",
                "relevant_memories": []
            }

        top_memory = relevant_entries[0]
        answer_text = (
            f"Based on institutional memory record [{top_memory.title}] recorded on {top_memory.timestamp}:\n\n"
            f"> {top_memory.content}\n\n"
            f"**Key context**: Category: `{top_memory.category}` | Related: `{', '.join(top_memory.related_tasks)}`"
        )

        return {
            "answer": answer_text,
            "relevant_memories": relevant_entries[:3]
        }
