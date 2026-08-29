"""
app.py
Project Sentinel: Predictive & Autonomous AI Project Manager
Streamlit Interactive Dashboard & Command Center
"""

import streamlit as st
import json
from datetime import datetime
from sentinel.sample_data import get_razorpay_project_state, get_ecommerce_project_state
from sentinel.orchestrator import SentinelOrchestrator
from sentinel.models import TaskStatus, ActionStatus, HealthTier


# Configure page settings
st.set_page_config(
    page_title="Project Sentinel | Autonomous Predictive AI PM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern glassmorphism aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .badge-critical {
        background-color: #EF444422;
        color: #EF4444;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        border: 1px solid #EF444455;
    }
    .badge-warning {
        background-color: #F59E0B22;
        color: #F59E0B;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        border: 1px solid #F59E0B55;
    }
    .badge-healthy {
        background-color: #10B98122;
        color: #10B981;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        border: 1px solid #10B98155;
    }
    .causal-step {
        background-color: #0F172A;
        border-left: 4px solid #3B82F6;
        padding: 12px 16px;
        margin-bottom: 12px;
        border-radius: 0 8px 8px 0;
    }
    .hitl-box {
        background: linear-gradient(135deg, #1E1B4B 0%, #1E293B 100%);
        border: 1px solid #6366F1;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "project_choice" not in st.session_state:
    st.session_state.project_choice = "Razorpay Payment Gateway Core Integration"

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = SentinelOrchestrator(get_razorpay_project_state())

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "🎯 Executive Dashboard"


# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.markdown("## **Project Sentinel**")
    st.caption("Autonomous & Predictive AI Project Manager")
    st.divider()

    st.markdown("### 📁 Project Dataset")
    selected_project = st.selectbox(
        "Choose Project Scenario",
        [
            "Razorpay Payment Gateway Core Integration",
            "Flash Sale Scalability & One-Click Checkout"
        ]
    )

    if selected_project != st.session_state.project_choice:
        st.session_state.project_choice = selected_project
        if "Razorpay" in selected_project:
            st.session_state.orchestrator.set_state(get_razorpay_project_state())
        else:
            st.session_state.orchestrator.set_state(get_ecommerce_project_state())
        st.rerun()

    st.divider()
    st.markdown("### ⚡ Fast Navigation")
    menu = st.radio(
        "Workflow Stage",
        [
            "🎯 Executive Dashboard",
            "🔮 1. Predictive Risk Engine",
            "🕵️ 2. Root Cause Investigator",
            "🤖 3. Autonomous Action Center",
            "🧠 4. What-If Scenario Sandbox",
            "👥 5. Team Workload & Burnout",
            "🔗 6. Dependency Intelligence & CPM",
            "📚 7. Project Institutional Memory"
        ]
    )

    st.divider()
    st.markdown("### ⚙️ Demo Actions")
    if st.button("🔄 Reset Project State"):
        if "Razorpay" in st.session_state.project_choice:
            st.session_state.orchestrator.set_state(get_razorpay_project_state())
        else:
            st.session_state.orchestrator.set_state(get_ecommerce_project_state())
        st.success("Project state reset to nominal demo baseline.")
        st.rerun()


# Run analysis cycle
orch = st.session_state.orchestrator
analysis = orch.run_full_cycle()
state = orch.state
health = analysis["health"]
risk = analysis["risk"]
root_cause = analysis["root_cause"]


# Top Header
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown(f"<div class='main-header'>🛡️ Project Sentinel: {state.name}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{state.description} • <b>Day {state.current_day} of {state.target_deadline_days}</b></div>", unsafe_allow_html=True)

with col_head2:
    tier_class = "badge-healthy" if health.tier == HealthTier.HEALTHY else ("badge-warning" if health.tier == HealthTier.NEEDS_ATTENTION else "badge-critical")
    tier_label = "🟢 HEALTHY" if health.tier == HealthTier.HEALTHY else ("🟡 NEEDS ATTENTION" if health.tier == HealthTier.NEEDS_ATTENTION else "🔴 CRITICAL RISK")
    st.markdown(f"<div style='text-align: right; padding-top: 10px;'><span class='{tier_class}' style='font-size: 1.1rem;'>{tier_label}</span></div>", unsafe_allow_html=True)


st.divider()


# ==========================================
# 1. EXECUTIVE DASHBOARD
# ==========================================
if menu == "🎯 Executive Dashboard":
    st.subheader("🎯 Executive Command Center")
    
    # Top KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="📈 Project Health Score",
            value=f"{health.overall_score} / 100",
            delta=f"{health.tier.value.replace('_', ' ')}"
        )
    with col2:
        st.metric(
            label="⚠️ Deadline Risk Probability",
            value=f"{risk.probability_of_delay}%",
            delta=f"{risk.deadline_risk_level} RISK",
            delta_color="inverse"
        )
    with col3:
        st.metric(
            label="⏱️ Predicted Slippage",
            value=f"+{risk.predicted_delay_days} days",
            delta=f"95% CI: [{risk.confidence_interval_95[0]}d, {risk.confidence_interval_95[1]}d]",
            delta_color="inverse"
        )
    with col4:
        st.metric(
            label="📊 Sprint Progress Drift",
            value=f"{risk.current_progress_pct}%",
            delta=f"Target: {risk.expected_progress_pct}% ({round(risk.current_progress_pct - risk.expected_progress_pct, 1)}%)",
            delta_color="normal"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Health Breakdown Grid
    col_dim, col_alerts = st.columns([1, 1])
    with col_dim:
        st.markdown("#### 📊 Multi-Dimensional Health Matrix")
        
        dimensions = [
            ("Schedule Health (25%)", health.schedule_score),
            ("Budget Health (15%)", health.budget_score),
            ("Resource Health (20%)", health.resources_score),
            ("Dependency Health (15%)", health.dependencies_score),
            ("Risk Health (15%)", health.risk_score),
            ("Quality Health (10%)", health.quality_score)
        ]
        
        for name, score in dimensions:
            bar_color = "🟢" if score >= 80 else ("🟡" if score >= 60 else "🔴")
            st.write(f"**{name}**: {score}/100 {bar_color}")
            st.progress(score / 100.0)

    with col_alerts:
        st.markdown("#### 🚨 Active Risk Triggers & Critical Alerts")
        for alert in health.alerts:
            st.error(f"⚠️ {alert}")
        for highlight in health.highlights:
            st.success(f"✅ {highlight}")

        st.info(f"💡 **Primary Bottleneck Vector**: {risk.primary_causes[0] if risk.primary_causes else 'Nominal'}")


# ==========================================
# 2. PREDICTIVE RISK ENGINE
# ==========================================
elif menu == "🔮 1. Predictive Risk Engine":
    st.subheader("🔮 Predictive Risk Detection (Monte Carlo Engine)")
    st.caption("Stochastic simulation of 2,500 delivery trajectories based on velocity variance and critical path dependencies.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### ⚠️ Predicted Deadline Risk Profile")
        
        st.markdown(f"""
        ```text
        ⚠️ Deadline Risk: {risk.deadline_risk_level}
        
        Current progress:  {risk.current_progress_pct}%
        Expected progress: {risk.expected_progress_pct}%
        
        Predicted delay:   {risk.predicted_delay_days} days
        Probability:       {risk.probability_of_delay}%
        
        Main cause:
        {risk.primary_causes[0] if risk.primary_causes else 'Nominal variance.'}
        ```
        """)

        st.write(f"**95% Confidence Delivery Range**: Day {risk.confidence_interval_95[0]} to Day {risk.confidence_interval_95[1]}")
        st.write(f"**Target Deadline**: Day {state.target_deadline_days}")

    with col2:
        st.markdown("### 📉 Simulation Trajectory Distribution")
        st.write(f"Based on **{risk.simulation_runs:,} Monte Carlo runs**, historical velocity **{state.historical_velocity_avg} pts/day (σ={state.historical_velocity_std})**.")
        
        sample_data = risk.trajectory_samples
        if sample_data:
            st.line_chart(sample_data, use_container_width=True)
            st.caption("Distribution of sampled project finish days (Baseline deadline is marked at Day " + str(state.target_deadline_days) + ")")

    st.divider()
    st.markdown("#### 🔍 Primary Delay Drivers")
    for i, cause in enumerate(risk.primary_causes, 1):
        st.warning(f"**Driver #{i}**: {cause}")


# ==========================================
# 3. ROOT CAUSE INVESTIGATOR
# ==========================================
elif menu == "🕵️ 2. Root Cause Investigator":
    st.subheader("🕵️ AI Root-Cause Investigator")
    st.caption("Autonomous causal graph traversal from observable sprint symptoms to core structural bottlenecks.")

    st.markdown(f"### 📋 Issue Summary: *{root_cause.issue_summary}*")
    st.info(f"🎯 **Investigation Confidence**: {root_cause.confidence_pct}%")

    st.markdown("### ⛓️ Causal Diagnostic Chain")
    for node in root_cause.chain:
        step_color = "#EF4444" if node.node_type == "ROOT_CAUSE" else ("#F59E0B" if node.node_type == "BOTTLENECK" else "#3B82F6")
        st.markdown(f"""
        <div class='causal-step' style='border-left-color: {step_color};'>
            <span style='color: {step_color}; font-weight: bold;'>STEP {node.step_number}: [{node.node_type}]</span><br>
            <b style='font-size: 1.1rem;'>{node.title}</b><br>
            <p style='margin: 4px 0;'>{node.description}</p>
            <small style='color: #94A3B8;'><b>Evidence:</b> {node.evidence}</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    col_root, col_int = st.columns([1, 1])
    with col_root:
        st.error(f"### 🎯 Root Cause Isolation\n\n{root_cause.root_cause_statement}")
    with col_int:
        st.success(f"### 💡 Recommended Targeted Intervention\n\n{root_cause.recommended_intervention}\n\n**Expected Leverage Impact:** {root_cause.estimated_leverage_impact}")


# ==========================================
# 4. AUTONOMOUS ACTION CENTER
# ==========================================
elif menu == "🤖 3. Autonomous Action Center":
    st.subheader("🤖 Autonomous Action Agent (Human-in-the-Loop)")
    st.caption("Review and approve AI-recommended corrective actions. Once approved, the agent executes them directly.")

    pending_actions = orch.action_agent.get_pending_actions()
    executed_actions = orch.action_agent.get_executed_actions()

    st.markdown(f"### ⏳ Pending Approval ({len(pending_actions)})")
    if not pending_actions:
        st.success("No pending actions. All recommended interventions have been resolved.")

    for action in pending_actions:
        with st.container():
            st.markdown(f"""
            <div class='hitl-box'>
                <div style='display: flex; justify-content: space-between;'>
                    <b style='font-size: 1.15rem; color: #818CF8;'>{action.title}</b>
                    <span class='badge-warning'>{action.urgency} URGENCY</span>
                </div>
                <p style='margin-top: 8px;'>{action.description}</p>
                <small style='color: #94A3B8;'>Type: <code>{action.action_type}</code> | Task Key: <code>{action.task_key or 'GLOBAL'}</code></small>
            </div>
            """, unsafe_allow_html=True)

            col_btn1, col_btn2, _ = st.columns([1, 1, 3])
            with col_btn1:
                if st.button(f"✅ Approve & Execute", key=f"app_{action.action_id}"):
                    res = orch.action_agent.approve_and_execute(action.action_id)
                    st.success(f"Executed: {res['summary']}")
                    st.rerun()
            with col_btn2:
                if st.button(f"❌ Reject", key=f"rej_{action.action_id}"):
                    orch.action_agent.reject_action(action.action_id)
                    st.warning("Action rejected.")
                    st.rerun()

    st.divider()
    st.markdown(f"### 📜 Execution & Audit Trail ({len(executed_actions)})")
    for act in executed_actions:
        st.markdown(f"**[{act.executed_at}]** `{act.status.value}` — **{act.title}**")
        st.caption(f"Result: {act.result_summary}")


# ==========================================
# 5. WHAT-IF SCENARIO SIMULATOR
# ==========================================
elif menu == "🧠 4. What-If Scenario Sandbox":
    st.subheader("🧠 What-If / Scenario Simulator")
    st.caption("Simulate team perturbations, developer absences, deadline shifts, and scope descoping in real time.")

    from sentinel.scenario_simulator import ScenarioSimulator
    sim = ScenarioSimulator(state)

    tab_dev, tab_deadline, tab_scope = st.tabs([
        "👤 Developer Absence",
        "📅 Deadline Adjustment",
        "✂️ Scope Descoping"
    ])

    with tab_dev:
        st.markdown("#### Scenario: What happens if a developer is unavailable?")
        dev_names = {d.id: d.name for d in state.developers.values()}
        sel_dev_id = st.selectbox("Select Developer", list(dev_names.keys()), format_func=lambda x: dev_names[x])
        absent_days = st.slider("Days Unavailable", min_value=1, max_value=14, value=5)

        if st.button("🧪 Run Developer Absence Simulation"):
            res = sim.simulate_developer_absence(sel_dev_id, absent_days)
            st.markdown(f"""
            ```text
            Scenario: {res.name}
            
            Expected delay:     +{res.delay_delta_days} days
            Budget impact:      +₹{int(res.cost_delta):,}
            Affected tasks:     {len(res.affected_tasks)} ({', '.join(res.affected_tasks)})
            Affected milestones: {len(res.affected_milestones)}
            
            Recommended:
            {res.recommendation}
            ```
            """)

    with tab_deadline:
        st.markdown("#### Scenario: What happens if we adjust the target deadline?")
        shift_days = st.slider("Deadline Shift (Days)", min_value=-7, max_value=14, value=3)

        if st.button("🧪 Run Deadline Shift Simulation"):
            res = sim.simulate_deadline_adjustment(shift_days)
            st.markdown(f"""
            ```text
            Scenario: {res.name}
            
            Expected completion: Day {res.simulated_completion_day}
            Delay relative to target: {res.delay_delta_days} days
            Risk direction: {res.risk_direction}
            
            Recommended:
            {res.recommendation}
            ```
            """)

    with tab_scope:
        st.markdown("#### Scenario: What if we drop non-essential tasks?")
        active_tasks = {t.id: f"[{t.key}] {t.title} ({t.story_points} pts)" for t in state.tasks.values() if t.status != TaskStatus.DONE}
        selected_drop_ids = st.multiselect("Select Tasks to Defer/Drop", list(active_tasks.keys()), format_func=lambda x: active_tasks[x])

        if st.button("🧪 Run Scope Reduction Simulation"):
            if selected_drop_ids:
                res = sim.simulate_scope_reduction(selected_drop_ids)
                st.markdown(f"""
                ```text
                Scenario: {res.name}
                
                Recovered timeline: {abs(res.delay_delta_days)} days faster
                Budget savings:     ₹{abs(int(res.cost_delta)):,}
                Deferred tasks:     {', '.join(res.affected_tasks)}
                
                Recommended:
                {res.recommendation}
                ```
                """)
            else:
                st.warning("Please select at least one task to drop.")


# ==========================================
# 6. TEAM WORKLOAD & BURNOUT
# ==========================================
elif menu == "👥 5. Team Workload & Burnout":
    st.subheader("👥 Team Workload & Burnout Risk (AI Resource Optimizer)")
    st.caption("Monitors capacity strain, context switching overhead, and auto-balances tasks across engineers.")

    workload_summary = analysis["team_workload"]
    rebalancing_recs = analysis["rebalancing_recommendations"]

    st.markdown("### 📊 Team Capacity & Burnout Matrix")
    for dev in workload_summary:
        col_name, col_bar, col_burnout = st.columns([2, 3, 2])
        with col_name:
            st.write(f"**{dev['name']}** ({dev['role']})")
            st.caption(f"{dev['assigned_points']} / {dev['capacity_points']} Story Points ({dev['status_label']})")
        with col_bar:
            st.progress(min(1.0, dev["workload_pct"] / 150.0))
            st.caption(f"Workload: {dev['workload_pct']}%")
        with col_burnout:
            b_color = "red" if dev['burnout_score'] > 70 else ("orange" if dev['burnout_score'] > 40 else "green")
            st.write(f"**Burnout Risk**: :{b_color}[{dev['burnout_score']}%]")
            st.caption(f"Active tasks: {dev['active_task_count']}")

    st.divider()
    st.markdown("### ⚖️ AI Automated Rebalancing Recommendations")
    if not rebalancing_recs:
        st.success("Workload is optimally distributed. No rebalancing transfers required.")

    for rec in rebalancing_recs:
        st.info(f"""
        **💡 Recommended Transfer:**
        - **Task**: [{rec['task_key']}] *{rec['task_title']}* ({rec['story_points']} story points)
        - **From**: **{rec['from_dev_name']}** ({rec['from_current_workload']}% → {rec['from_projected_workload']}%)
        - **To**: **{rec['to_dev_name']}** ({rec['to_current_workload']}% → {rec['to_projected_workload']}%)
        - **Impact**: {rec['reasoning']}
        """)


# ==========================================
# 7. DEPENDENCY INTELLIGENCE & CPM
# ==========================================
elif menu == "🔗 6. Dependency Intelligence & CPM":
    st.subheader("🔗 Dependency Intelligence & Critical Path Method (CPM)")
    st.caption("DAG analysis identifies bottleneck chains, zero-slack critical paths, and upstream delay propagation.")

    tree_summary = analysis["dependency_tree"]
    critical_path = analysis["critical_path"]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 🚨 Critical Path Tasks")
        st.write("Tasks with **Zero Slack** that directly dictate final delivery date:")
        for cp_id in critical_path:
            task = state.tasks.get(cp_id)
            if task:
                st.error(f"⚡ **[{task.key}]** {task.title} ({task.remaining_days}d remaining)")

    with col2:
        st.markdown("### 📋 Complete Dependency Registry")
        table_data = []
        for t in tree_summary:
            table_data.append({
                "Key": t["key"],
                "Title": t["title"],
                "Status": t["status"],
                "Dependencies": ", ".join(t["dependencies"]) or "None",
                "Downstream": ", ".join(t["downstream"]) or "None",
                "Critical?": "⚡ YES" if t["is_critical"] else "NO",
                "Slack (days)": t["slack"]
            })
        st.dataframe(table_data, use_container_width=True)

    st.divider()
    st.markdown("### 🌊 Interactive Cascade Delay Simulator")
    selected_task_key = st.selectbox("Select Task to Test Delay Impact", [t.key for t in state.tasks.values()])
    test_delay = st.slider("Simulated Task Delay (Days)", 1, 10, 3)

    from sentinel.dependency_engine import DependencyEngine
    dep_engine = DependencyEngine(state)
    target_task_id = next(tid for tid, t in state.tasks.items() if t.key == selected_task_key)
    cascade = dep_engine.calculate_cascade_impact(target_task_id, float(test_delay))

    st.markdown(f"""
    - **Delayed Task**: `[{cascade['delayed_task_key']}]` (+{cascade['delay_days']} days)
    - **Downstream Tasks Impacted**: `{cascade['affected_downstream_count']}`
    - **Project-Level Delay Delta**: `+{cascade['project_delay_delta']} days`
    - **Critical Path Task?**: `{'YES (Direct Schedule Impact)' if cascade['is_critical_task'] else 'NO (Absorbed by Slack)'}`
    """)


# ==========================================
# 8. PROJECT INSTITUTIONAL MEMORY
# ==========================================
elif menu == "📚 7. Project Institutional Memory":
    st.subheader("📚 Project Institutional Memory")
    st.caption("Long-term memory retaining Architectural Decision Records (ADRs), incident post-mortems, and lessons learned.")

    memory_store = orch.memory

    tab_ask, tab_browse, tab_add = st.tabs([
        "💬 Ask Memory Assistant",
        "📖 Browse Records",
        "➕ Add New Memory Record"
    ])

    with tab_ask:
        st.markdown("#### Query Institutional Memory")
        user_query = st.text_input(
            "Ask a question about previous decisions, incidents, or architecture:",
            value="Why did we choose Razorpay over Stripe for payments?"
        )

        if st.button("🔍 Search Institutional Memory"):
            ans = memory_store.answer_question(user_query)
            st.markdown(ans["answer"])

    with tab_browse:
        st.markdown(f"#### Institutional Knowledge Base ({len(memory_store.entries)} Records)")
        for entry in memory_store.entries:
            with st.expander(f"[{entry.category}] {entry.title} ({entry.timestamp})"):
                st.write(entry.content)
                st.caption(f"Tags: {', '.join(entry.tags)} | Related Tasks: {', '.join(entry.related_tasks)}")

    with tab_add:
        st.markdown("#### Add New Decision / Lesson Learned")
        new_cat = st.selectbox("Category", ["DECISION", "INCIDENT", "ARCHITECTURE", "LESSON_LEARNED", "STAKEHOLDER_PREF"])
        new_title = st.text_input("Title")
        new_content = st.text_area("Content / Rationale")
        new_tags = st.text_input("Tags (comma separated)", "payments, architecture")

        if st.button("💾 Save to Project Memory"):
            if new_title and new_content:
                entry = memory_store.add_entry(
                    category=new_cat,
                    title=new_title,
                    content=new_content,
                    tags=[t.strip() for t in new_tags.split(",")]
                )
                st.success(f"Saved memory record '{entry.title}' successfully.")
                st.rerun()
            else:
                st.warning("Please fill in both title and content.")
