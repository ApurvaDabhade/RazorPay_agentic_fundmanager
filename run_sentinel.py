"""
run_sentinel.py
CLI Runner for Project Sentinel: Autonomous & Predictive AI Project Manager
Executes the full 5-step cycle directly in the terminal.
"""

import sys
from sentinel.orchestrator import SentinelOrchestrator
from sentinel.sample_data import get_razorpay_project_state


def main():
    print("=" * 75)
    print("🛡️  PROJECT SENTINEL: AUTONOMOUS & PREDICTIVE AI PROJECT MANAGER")
    print("=" * 75)

    orch = SentinelOrchestrator(get_razorpay_project_state())
    analysis = orch.run_full_cycle()
    state = orch.state

    print(f"\n📂 Project: {state.name}")
    print(f"📝 Description: {state.description}")
    print(f"⏱️ Timeline: Day {state.current_day} of {state.target_deadline_days} | Allocated Budget: ₹{int(state.budget_allocated):,}")
    print("-" * 75)

    # 1. Executive Health & Predictive Risk
    health = analysis["health"]
    risk = analysis["risk"]

    print("\n📈 [EXECUTIVE DASHBOARD & HEALTH SCORE]")
    print(f"   Project Health Score: {health.overall_score}/100 [{health.tier.value}]")
    print(f"   ├── Schedule Health:     {health.schedule_score}/100")
    print(f"   ├── Budget Health:       {health.budget_score}/100")
    print(f"   ├── Resource Health:     {health.resources_score}/100")
    print(f"   ├── Dependency Health:   {health.dependencies_score}/100")
    print(f"   ├── Risk Health:         {health.risk_score}/100")
    print(f"   └── Quality Health:      {health.quality_score}/100")

    # 2. Step 1: Predict
    print("\n" + "=" * 75)
    print("🔮 STEP 1: PREDICTIVE RISK DETECTION (MONTE CARLO ENGINE)")
    print("=" * 75)
    print(f"   ⚠️  Deadline Risk Level:   {risk.deadline_risk_level}")
    print(f"   📊 Current Progress:       {risk.current_progress_pct}% (Expected: {risk.expected_progress_pct}%)")
    print(f"   ⏱️  Predicted Delay:        +{risk.predicted_delay_days} days")
    print(f"   🎲 Probability of Delay:   {risk.probability_of_delay}% (across {risk.simulation_runs:,} runs)")
    print(f"   🎯 95% Confidence Bounds:  Day {risk.confidence_interval_95[0]} to Day {risk.confidence_interval_95[1]}")
    print("   🔍 Primary Root Cause Drivers:")
    for cause in risk.primary_causes:
        print(f"      • {cause}")

    # 3. Step 2: Investigate
    root_cause = analysis["root_cause"]
    print("\n" + "=" * 75)
    print("🕵️ STEP 2: AI ROOT-CAUSE INVESTIGATOR")
    print("=" * 75)
    print(f"   📋 Issue Summary: {root_cause.issue_summary}")
    print("   ⛓️  Causal Graph Breakdown:")
    for node in root_cause.chain:
        print(f"      Step {node.step_number} [{node.node_type}]: {node.title}")
        print(f"             └─ {node.description}")
    print(f"\n   🎯 Isolated Root Cause: {root_cause.root_cause_statement}")
    print(f"   💡 Targeted Intervention: {root_cause.recommended_intervention}")
    print(f"   ⚡ Estimated Leverage Impact: {root_cause.estimated_leverage_impact}")

    # 4. Step 3: Simulate
    scenarios = analysis["scenarios"]
    print("\n" + "=" * 75)
    print("🧠 STEP 3: WHAT-IF / SCENARIO SIMULATOR")
    print("=" * 75)
    for sc in scenarios:
        print(f"   🧪 Scenario: {sc.name}")
        print(f"      • Projected Delay Impact: +{sc.delay_delta_days} days")
        print(f"      • Projected Budget Delta: +₹{int(sc.cost_delta):,}")
        print(f"      • Affected Tasks: {', '.join(sc.affected_tasks)}")
        print(f"      • Recommendation: {sc.recommendation}\n")

    # 5. Step 4: Recommend (Resource Optimizer)
    workload = analysis["team_workload"]
    rebalancing = analysis["rebalancing_recommendations"]
    print("=" * 75)
    print("👥 STEP 4: TEAM WORKLOAD & AI RESOURCE OPTIMIZER")
    print("=" * 75)
    for dev in workload:
        print(f"   👤 {dev['name']:<18} | Workload: {dev['workload_pct']:>5.1f}% | Burnout Risk: {dev['burnout_score']:>4.1f}% | Status: {dev['status_label']}")
    
    print("\n   ⚖️  AI Task Rebalancing Recommendations:")
    for rec in rebalancing:
        print(f"      • Reassign [{rec['task_key']}] '{rec['task_title']}' ({rec['story_points']} pts)")
        print(f"        From: {rec['from_dev_name']} ({rec['from_current_workload']}% → {rec['from_projected_workload']}%)")
        print(f"        To:   {rec['to_dev_name']} ({rec['to_current_workload']}% → {rec['to_projected_workload']}%)")
        print(f"        Rationale: {rec['reasoning']}")

    # 6. Step 5: Act (Human-in-the-Loop)
    pending_actions = analysis["pending_actions"]
    print("\n" + "=" * 75)
    print("🤖 STEP 5: AUTONOMOUS ACTION AGENT (HUMAN-IN-THE-LOOP)")
    print("=" * 75)
    print(f"   Pending Interventions ({len(pending_actions)}):")
    for act in pending_actions:
        print(f"   [ ] {act.action_id}: {act.title} [{act.urgency} URGENCY]")
        print(f"       └─ {act.description}")

    # Simulate automatic 1st action approval execution for demonstration
    if pending_actions:
        first_act = pending_actions[0]
        print(f"\n   ⚙️  Simulating Human Approval on '{first_act.action_id}'...")
        exec_res = orch.action_agent.approve_and_execute(first_act.action_id)
        print(f"   ✅ Execution Result: {exec_res['summary']}")

    # 7. Project Institutional Memory
    print("\n" + "=" * 75)
    print("📚 PROJECT INSTITUTIONAL MEMORY")
    print("=" * 75)
    q = "Why did we choose Razorpay over Stripe for payments?"
    print(f"   ❓ Query: '{q}'")
    ans = orch.memory.answer_question(q)
    print(f"   💬 Answer:\n{ans['answer']}")
    print("\n" + "=" * 75)
    print("✨ Sentinel Cycle Completed Successfully!")
    print("=" * 75)


if __name__ == "__main__":
    main()
