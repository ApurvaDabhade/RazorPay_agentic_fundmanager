"""
app.py
Project Sentinel: Next-Gen Autonomous & Predictive AI Project Manager
Ultra-Modern Glassmorphic Streamlit Dashboard with Plotly Visual Analytics
"""

import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from sentinel.sample_data import get_razorpay_project_state, get_ecommerce_project_state
from sentinel.orchestrator import SentinelOrchestrator
from sentinel.models import TaskStatus, ActionStatus, HealthTier
from sentinel.scenario_simulator import ScenarioSimulator
from sentinel.dependency_engine import DependencyEngine


# Set Page Config
st.set_page_config(
    page_title="Project Sentinel | Autonomous Predictive AI PM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End SaaS Dark Theme & Glassmorphism CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0B0F19 0%, #0F172A 100%);
        color: #F8FAFC;
    }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    
    .hero-sub {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 20px;
    }
    
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #34D399;
        border-radius: 50%;
        box-shadow: 0 0 10px #34D399;
    }
    
    .causal-node {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        position: relative;
    }
    
    .causal-arrow {
        text-align: center;
        color: #6366F1;
        font-size: 1.4rem;
        margin: -6px 0 8px 0;
        font-weight: bold;
    }
    
    .tag-critical {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .tag-high {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .tag-optimal {
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .tag-success {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .hitl-container {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "project_choice" not in st.session_state:
    st.session_state.project_choice = "Razorpay Payment Gateway Core Integration"

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = SentinelOrchestrator(get_razorpay_project_state())


# Sidebar Configuration
with st.sidebar:
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
        <span style='font-size: 2.2rem;'>🛡️</span>
        <div>
            <div style='font-size: 1.3rem; font-weight: 800; color: #F8FAFC;'>Sentinel AI</div>
            <div style='font-size: 0.75rem; color: #818CF8; font-weight: 600;'>AUTONOMOUS PM AGENT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='live-badge'><div class='pulse-dot'></div>SYSTEM ONLINE (LIVE)</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 🎯 Active Project")
    selected_project = st.selectbox(
        "Choose Project Dataset",
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
    st.markdown("### 🧭 Intelligence Navigation")
    menu = st.radio(
        "Select View",
        [
            "🎯 Executive Command Center",
            "🔮 1. Predictive Risk Engine",
            "🕵️ 2. Root Cause Investigator",
            "🤖 3. Autonomous Action Center",
            "🧠 4. What-If Scenario Sandbox",
            "👥 5. Team Workload & Burnout",
            "🔗 6. Dependency DAG & Critical Path",
            "📚 7. Project Institutional Memory"
        ]
    )

    st.divider()
    st.markdown("### ⚙️ Quick Actions")
    if st.button("🔄 Reset Project Baseline", use_container_width=True):
        if "Razorpay" in st.session_state.project_choice:
            st.session_state.orchestrator.set_state(get_razorpay_project_state())
        else:
            st.session_state.orchestrator.set_state(get_ecommerce_project_state())
        st.success("Project state reset.")
        st.rerun()

    st.caption("Powered by Sentinel Multi-Agent Core Engine • MIT License")


# Run Orchestrator Analysis Cycle
orch = st.session_state.orchestrator
analysis = orch.run_full_cycle()
state = orch.state
health = analysis["health"]
risk = analysis["risk"]
root_cause = analysis["root_cause"]


# Top Banner & Global Stats
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"<div class='hero-title'>🛡️ {state.name}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-sub'>{state.description} • <b>Day {state.current_day} of {state.target_deadline_days}</b> • Budget: <b>₹{int(state.budget_allocated):,}</b></div>", unsafe_allow_html=True)

with col_h2:
    if health.tier == HealthTier.HEALTHY:
        status_html = "<span class='tag-success' style='font-size: 1rem; padding: 6px 14px;'>🟢 HEALTHY (80-100)</span>"
    elif health.tier == HealthTier.NEEDS_ATTENTION:
        status_html = "<span class='tag-high' style='font-size: 1rem; padding: 6px 14px;'>🟡 NEEDS ATTENTION</span>"
    else:
        status_html = "<span class='tag-critical' style='font-size: 1rem; padding: 6px 14px;'>🔴 CRITICAL RISK</span>"
    st.markdown(f"<div style='text-align: right; padding-top: 8px;'>{status_html}</div>", unsafe_allow_html=True)


# =========================================================================
# 1. EXECUTIVE COMMAND CENTER
# =========================================================================
if menu == "🎯 Executive Command Center":
    st.markdown("### 🎯 Executive Health & Risk Overview")
    
    # 4 KPI Cards
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.markdown(f"""
        <div class='glass-card' style='border-top: 3px solid #6366F1;'>
            <div style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>PROJECT HEALTH SCORE</div>
            <div style='font-size: 2.2rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;'>{health.overall_score}<span style='font-size: 1.1rem; color: #64748B;'>/100</span></div>
            <div style='font-size: 0.8rem; color: #818CF8;'>Multi-Dimensional Weighted</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k2:
        st.markdown(f"""
        <div class='glass-card' style='border-top: 3px solid #EF4444;'>
            <div style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>DEADLINE FAILURE RISK</div>
            <div style='font-size: 2.2rem; font-weight: 800; color: #EF4444; margin: 4px 0;'>{risk.probability_of_delay}%</div>
            <div style='font-size: 0.8rem; color: #F87171;'>Monte Carlo (2,500 runs)</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k3:
        st.markdown(f"""
        <div class='glass-card' style='border-top: 3px solid #F59E0B;'>
            <div style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>PREDICTED SLIPPAGE</div>
            <div style='font-size: 2.2rem; font-weight: 800; color: #FBBF24; margin: 4px 0;'>+{risk.predicted_delay_days}d</div>
            <div style='font-size: 0.8rem; color: #FDE68A;'>95% CI: [{risk.confidence_interval_95[0]}d, {risk.confidence_interval_95[1]}d]</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k4:
        st.markdown(f"""
        <div class='glass-card' style='border-top: 3px solid #10B981;'>
            <div style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>PROGRESS DRIFT</div>
            <div style='font-size: 2.2rem; font-weight: 800; color: #34D399; margin: 4px 0;'>{risk.current_progress_pct}%</div>
            <div style='font-size: 0.8rem; color: #94A3B8;'>Target Baseline: {risk.expected_progress_pct}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Plotly Visuals: Health Radar & Gauge
    col_g1, col_g2 = st.columns([1, 1])
    
    with col_g1:
        st.markdown("#### 🧭 Multi-Dimensional Health Radar")
        radar_categories = ['Schedule', 'Budget', 'Resources', 'Dependencies', 'Risk', 'Quality']
        radar_values = [
            health.schedule_score,
            health.budget_score,
            health.resources_score,
            health.dependencies_score,
            health.risk_score,
            health.quality_score
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_values + [radar_values[0]],
            theta=radar_categories + [radar_categories[0]],
            fill='toself',
            fillcolor='rgba(99, 102, 241, 0.35)',
            line=dict(color='#818CF8', width=2),
            name='Health Breakdown'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color='#64748B'),
                angularaxis=dict(color='#94A3B8')
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=20, b=20),
            height=320
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_g2:
        st.markdown("#### 🚨 Active Alerts & Tactical Insights")
        for alert in health.alerts:
            st.markdown(f"<div class='tag-critical' style='display: block; margin-bottom: 8px; padding: 10px 14px; font-size: 0.9rem;'>⚠️ {alert}</div>", unsafe_allow_html=True)
        for h_item in health.highlights:
            st.markdown(f"<div class='tag-success' style='display: block; margin-bottom: 8px; padding: 10px 14px; font-size: 0.9rem;'>✅ {h_item}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='glass-card' style='padding: 16px; margin-top: 14px; border-left: 4px solid #6366F1;'>
            <b style='color: #818CF8;'>💡 Sentinel Recommendation:</b><br>
            <span style='color: #CBD5E1;'>{root_cause.recommended_intervention}</span>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# 2. PREDICTIVE RISK ENGINE
# =========================================================================
elif menu == "🔮 1. Predictive Risk Engine":
    st.markdown("### 🔮 Predictive Risk Detection Engine (Monte Carlo)")
    st.caption("Stochastic simulation of 2,500 delivery trajectories factoring in velocity uncertainty and dependency chain locks.")

    col_p1, col_p2 = st.columns([1, 1])
    with col_p1:
        st.markdown(f"""
        <div class='glass-card'>
            <h4 style='color: #F87171; margin-top: 0;'>⚠️ Predicted Deadline Risk: {risk.deadline_risk_level}</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 16px 0;'>
                <div>
                    <span style='color: #94A3B8; font-size: 0.85rem;'>Current Progress</span><br>
                    <b style='font-size: 1.3rem; color: #F8FAFC;'>{risk.current_progress_pct}%</b>
                </div>
                <div>
                    <span style='color: #94A3B8; font-size: 0.85rem;'>Expected Progress</span><br>
                    <b style='font-size: 1.3rem; color: #F8FAFC;'>{risk.expected_progress_pct}%</b>
                </div>
                <div>
                    <span style='color: #94A3B8; font-size: 0.85rem;'>Predicted Delay</span><br>
                    <b style='font-size: 1.3rem; color: #EF4444;'>+{risk.predicted_delay_days} days</b>
                </div>
                <div>
                    <span style='color: #94A3B8; font-size: 0.85rem;'>Failure Probability</span><br>
                    <b style='font-size: 1.3rem; color: #EF4444;'>{risk.probability_of_delay}%</b>
                </div>
            </div>
            <div style='background: rgba(15, 23, 42, 0.8); padding: 12px; border-radius: 8px;'>
                <b style='color: #818CF8;'>Primary Root Bottleneck:</b><br>
                <span style='color: #E2E8F0; font-size: 0.9rem;'>{risk.primary_causes[0] if risk.primary_causes else 'Nominal.'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("#### 📉 Monte Carlo Simulation Trajectory Distribution")
        samples = risk.trajectory_samples
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=samples,
            nbinsx=25,
            marker_color='#6366F1',
            opacity=0.75,
            name='Simulation Runs'
        ))
        fig_hist.add_vline(
            x=state.target_deadline_days,
            line_width=3,
            line_dash="dash",
            line_color="#EF4444",
            annotation_text=f"Target Deadline (Day {state.target_deadline_days})",
            annotation_position="top right"
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Project Completion (Days)", color='#94A3B8', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="Frequency", color='#94A3B8', gridcolor='rgba(255,255,255,0.05)'),
            margin=dict(l=40, r=20, t=30, b=40),
            height=300
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("#### 🔍 Delay Driver Breakdown")
    for i, cause in enumerate(risk.primary_causes, 1):
        st.markdown(f"<div class='tag-high' style='display: block; margin-bottom: 8px; padding: 10px 14px; font-size: 0.9rem;'><b>Driver #{i}</b>: {cause}</div>", unsafe_allow_html=True)


# =========================================================================
# 3. ROOT CAUSE INVESTIGATOR
# =========================================================================
elif menu == "🕵️ 2. Root Cause Investigator":
    st.markdown("### 🕵️ AI Root-Cause Investigator")
    st.caption("Autonomous multi-hop causal graph traversal diagnosing the structural root cause of project delay.")

    st.markdown(f"**Issue Summary**: *{root_cause.issue_summary}* • <span class='tag-optimal'>Confidence: {root_cause.confidence_pct}%</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Render Visual Causal Stepper
    for idx, node in enumerate(root_cause.chain):
        color = "#EF4444" if node.node_type == "ROOT_CAUSE" else ("#F59E0B" if node.node_type == "BOTTLENECK" else "#6366F1")
        border_class = f"border-left: 4px solid {color};"
        st.markdown(f"""
        <div class='causal-node' style='{border_class}'>
            <div style='display: flex; justify-content: space-between;'>
                <b style='color: {color}; font-size: 0.85rem;'>STEP {node.step_number} • [{node.node_type}]</b>
                <span class='tag-high'>{node.severity} IMPACT</span>
            </div>
            <div style='font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin: 4px 0;'>{node.title}</div>
            <p style='color: #CBD5E1; margin: 4px 0 8px 0; font-size: 0.95rem;'>{node.description}</p>
            <div style='font-size: 0.85rem; color: #94A3B8;'><b>Evidence:</b> {node.evidence}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if idx < len(root_cause.chain) - 1:
            st.markdown("<div class='causal-arrow'>↓</div>", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns([1, 1])
    with col_r1:
        st.markdown(f"""
        <div class='glass-card' style='border-left: 4px solid #EF4444;'>
            <h4 style='color: #F87171; margin-top: 0;'>🎯 Root Cause Statement</h4>
            <p style='color: #E2E8F0; font-size: 0.95rem;'>{root_cause.root_cause_statement}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_r2:
        st.markdown(f"""
        <div class='glass-card' style='border-left: 4px solid #10B981;'>
            <h4 style='color: #34D399; margin-top: 0;'>💡 Targeted Leverage Intervention</h4>
            <p style='color: #E2E8F0; font-size: 0.95rem;'>{root_cause.recommended_intervention}</p>
            <small style='color: #818CF8;'><b>Impact:</b> {root_cause.estimated_leverage_impact}</small>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# 4. AUTONOMOUS ACTION CENTER
# =========================================================================
elif menu == "🤖 3. Autonomous Action Center":
    st.markdown("### 🤖 Autonomous Action Agent (Human-in-the-Loop)")
    st.caption("Inspect and approve AI-generated corrective actions. Approved actions immediately execute and sync across state and Jira.")

    pending_actions = orch.action_agent.get_pending_actions()
    executed_actions = orch.action_agent.get_executed_actions()

    st.markdown(f"#### ⏳ Interventions Awaiting Approval ({len(pending_actions)})")
    if not pending_actions:
        st.markdown("<div class='tag-success' style='display: block; padding: 14px; font-size: 1rem;'>✅ All recommended actions have been resolved!</div>", unsafe_allow_html=True)

    for action in pending_actions:
        st.markdown(f"""
        <div class='hitl-container'>
            <div style='display: flex; justify-content: space-between;'>
                <b style='font-size: 1.15rem; color: #A5B4FC;'>{action.title}</b>
                <span class='tag-high'>{action.urgency} PRIORITY</span>
            </div>
            <p style='color: #CBD5E1; margin: 8px 0;'>{action.description}</p>
            <div style='font-size: 0.8rem; color: #94A3B8;'>Action Type: <code>{action.action_type}</code> | Task Key: <code>{action.task_key or 'GLOBAL'}</code></div>
        </div>
        """, unsafe_allow_html=True)

        col_a1, col_a2, _ = st.columns([1.2, 1, 3])
        with col_a1:
            if st.button(f"✅ Approve & Execute", key=f"btn_app_{action.action_id}", type="primary"):
                res = orch.action_agent.approve_and_execute(action.action_id)
                st.success(f"Executed: {res['summary']}")
                st.rerun()
        with col_a2:
            if st.button(f"❌ Reject", key=f"btn_rej_{action.action_id}"):
                orch.action_agent.reject_action(action.action_id)
                st.warning("Action rejected.")
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"#### 📜 Execution & Audit Log ({len(executed_actions)})")
    for act in executed_actions:
        status_color = "#34D399" if act.status == ActionStatus.EXECUTED else "#EF4444"
        st.markdown(f"""
        <div style='background: rgba(15, 23, 42, 0.6); border-left: 3px solid {status_color}; padding: 12px 16px; border-radius: 6px; margin-bottom: 8px;'>
            <b>[{act.executed_at}]</b> <span style='color: {status_color}; font-weight: bold;'>{act.status.value}</span> — <b>{act.title}</b><br>
            <small style='color: #94A3B8;'>Result: {act.result_summary}</small>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# 5. WHAT-IF SCENARIO SANDBOX
# =========================================================================
elif menu == "🧠 4. What-If Scenario Sandbox":
    st.markdown("### 🧠 What-If / Scenario Simulator Sandbox")
    st.caption("Run discrete-event simulations on resource shocks, scope adjustments, and deadline compression.")

    sim = ScenarioSimulator(state)
    tab1, tab2, tab3 = st.tabs(["👤 Developer Absence Shock", "📅 Deadline Shift", "✂️ Scope Descoping"])

    with tab1:
        st.markdown("#### Simulate Developer Unavailability")
        dev_map = {d.id: f"{d.name} ({d.role})" for d in state.developers.values()}
        sel_dev = st.selectbox("Select Developer", list(dev_map.keys()), format_func=lambda x: dev_map[x])
        absence_days = st.slider("Duration of Absence (Days)", min_value=1, max_value=14, value=5)

        if st.button("🧪 Simulate Developer Absence", type="primary"):
            res = sim.simulate_developer_absence(sel_dev, absence_days)
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("⏱️ Projected Delay", f"+{res.delay_delta_days} days", delta="Slippage", delta_color="inverse")
            with col_s2:
                st.metric("💰 Budget Impact", f"+₹{int(res.cost_delta):,}", delta="Burn rate cost", delta_color="inverse")
            with col_s3:
                st.metric("📋 Affected Tasks", f"{len(res.affected_tasks)} items", delta=", ".join(res.affected_tasks))
            
            st.info(f"💡 **AI Recommendation**: {res.recommendation}")

    with tab2:
        st.markdown("#### Simulate Deadline Adjustments")
        shift = st.slider("Shift Deadline (Days)", min_value=-7, max_value=14, value=3)

        if st.button("🧪 Simulate Deadline Adjustment", type="primary"):
            res = sim.simulate_deadline_adjustment(shift)
            st.metric("Projected Completion Day", f"Day {res.simulated_completion_day}", delta=f"{res.risk_direction} RISK")
            st.info(f"💡 **Recommendation**: {res.recommendation}")

    with tab3:
        st.markdown("#### Simulate Scope Descoping")
        active_tasks = {t.id: f"[{t.key}] {t.title} ({t.story_points} pts)" for t in state.tasks.values() if t.status != TaskStatus.DONE}
        drop_ids = st.multiselect("Select Candidate Tasks to Defer", list(active_tasks.keys()), format_func=lambda x: active_tasks[x])

        if st.button("🧪 Simulate Scope Descoping", type="primary"):
            if drop_ids:
                res = sim.simulate_scope_reduction(drop_ids)
                col_sc1, col_sc2 = st.columns(2)
                with col_sc1:
                    st.metric("⏱️ Recovered Time", f"{abs(res.delay_delta_days)} days faster", delta="Timeline Recovery")
                with col_sc2:
                    st.metric("💰 Budget Savings", f"₹{abs(int(res.cost_delta)):,}", delta="Saved Burn")
                st.success(f"💡 **Recommendation**: {res.recommendation}")
            else:
                st.warning("Please select at least one task.")


# =========================================================================
# 6. TEAM WORKLOAD & BURNOUT
# =========================================================================
elif menu == "👥 5. Team Workload & Burnout":
    st.markdown("### 👥 Team Workload & AI Resource Optimizer")
    st.caption("Real-time workload distribution analysis, burnout risk scoring, and automatic task rebalancing.")

    workload_data = analysis["team_workload"]
    rebalancing_recs = analysis["rebalancing_recommendations"]

    # Visual Bar Chart of Workloads
    names = [d["name"] for d in workload_data]
    workloads = [d["workload_pct"] for d in workload_data]
    colors = ['#EF4444' if w > 105 else ('#34D399' if w < 60 else '#60A5FA') for w in workloads]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=names,
        y=workloads,
        marker_color=colors,
        text=[f"{w}%" for w in workloads],
        textposition='outside'
    ))
    fig_bar.add_hline(y=100, line_dash="dash", line_color="#EF4444", annotation_text="100% Safe Capacity Threshold")
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title="Workload Utilization (%)", color='#94A3B8', gridcolor='rgba(255,255,255,0.05)'),
        xaxis=dict(color='#94A3B8'),
        margin=dict(l=40, r=20, t=20, b=40),
        height=320
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### ⚖️ AI Optimal Task Rebalancing Matrix")
    if not rebalancing_recs:
        st.success("Workload is balanced across all team members.")

    for rec in rebalancing_recs:
        st.markdown(f"""
        <div class='glass-card' style='border-left: 4px solid #6366F1;'>
            <b style='color: #818CF8; font-size: 1.1rem;'>💡 Suggested Reassignment: [{rec['task_key']}] {rec['task_title']} ({rec['story_points']} pts)</b><br>
            <div style='margin: 8px 0; color: #CBD5E1;'>
                • <b>From</b>: <span style='color: #F87171;'>{rec['from_dev_name']}</span> ({rec['from_current_workload']}% → {rec['from_projected_workload']}%)<br>
                • <b>To</b>: <span style='color: #34D399;'>{rec['to_dev_name']}</span> ({rec['to_current_workload']}% → {rec['to_projected_workload']}%)<br>
                • <b>Impact Rationale</b>: {rec['reasoning']}
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# 7. DEPENDENCY DAG & CRITICAL PATH
# =========================================================================
elif menu == "🔗 6. Dependency DAG & Critical Path":
    st.markdown("### 🔗 Dependency DAG & Critical Path Method (CPM)")
    st.caption("Zero-slack critical path identification and upstream delay cascade simulation.")

    tree_summary = analysis["dependency_tree"]
    critical_path = analysis["critical_path"]

    col_cp1, col_cp2 = st.columns([1, 2])
    with col_cp1:
        st.markdown("#### ⚡ Critical Path Tasks (Zero Slack)")
        for cp_id in critical_path:
            t = state.tasks.get(cp_id)
            if t:
                st.markdown(f"<div class='tag-critical' style='display: block; margin-bottom: 8px; padding: 10px;'>⚡ <b>[{t.key}]</b> {t.title} ({t.remaining_days}d rem)</div>", unsafe_allow_html=True)

    with col_cp2:
        st.markdown("#### 📋 Task Dependency Registry")
        table_rows = []
        for t in tree_summary:
            table_rows.append({
                "Key": t["key"],
                "Title": t["title"],
                "Status": t["status"],
                "Dependencies": ", ".join(t["dependencies"]) or "None",
                "Critical Path?": "⚡ YES" if t["is_critical"] else "NO",
                "Slack": f"{t['slack']}d"
            })
        st.dataframe(table_rows, use_container_width=True)

    st.divider()
    st.markdown("#### 🌊 Cascade Delay Impact Test")
    target_key = st.selectbox("Select Task to Inject Delay", [t.key for t in state.tasks.values()])
    delay_input = st.slider("Simulated Delay (Days)", 1, 10, 3)

    dep_engine = DependencyEngine(state)
    t_id = next(tid for tid, t in state.tasks.items() if t.key == target_key)
    cascade_res = dep_engine.calculate_cascade_impact(t_id, float(delay_input))

    st.markdown(f"""
    <div class='glass-card'>
        • <b>Target Task</b>: <code>[{cascade_res['delayed_task_key']}]</code> (+{cascade_res['delay_days']} days)<br>
        • <b>Downstream Tasks Affected</b>: <b>{cascade_res['affected_downstream_count']}</b><br>
        • <b>Project-Level Delay Delta</b>: <b style='color: #EF4444;'>+{cascade_res['project_delay_delta']} days</b><br>
        • <b>Critical Path Task?</b>: <b>{'YES (Directly delays final delivery)' if cascade_res['is_critical_task'] else 'NO (Absorbed by Slack)'}</b>
    </div>
    """, unsafe_allow_html=True)


# =========================================================================
# 8. PROJECT INSTITUTIONAL MEMORY
# =========================================================================
elif menu == "📚 7. Project Institutional Memory":
    st.markdown("### 📚 Project Institutional Memory & Knowledge Base")
    st.caption("Long-term storage of Architectural Decision Records (ADRs), incident post-mortems, and stakeholder constraints.")

    memory_store = orch.memory
    m_tab1, m_tab2 = st.tabs(["💬 Query Memory Assistant", "📖 Browse All Records"])

    with m_tab1:
        st.markdown("#### Ask Sentinel about Past Decisions & Incidents")
        q_options = [
            "Why did we choose Razorpay over Stripe for payments?",
            "What was the Redis webhook incident in Sprint 2?",
            "What is the VP of Product zero downtime constraint?"
        ]
        sel_q = st.selectbox("Quick Query Presets", q_options)
        custom_q = st.text_input("Or write your custom query:", value=sel_q)

        if st.button("🔍 Search Institutional Memory", type="primary"):
            ans = memory_store.answer_question(custom_q)
            st.markdown(f"""
            <div class='glass-card' style='border-left: 4px solid #6366F1;'>
                {ans['answer']}
            </div>
            """, unsafe_allow_html=True)

    with m_tab2:
        st.markdown(f"#### All Stored Knowledge Records ({len(memory_store.entries)})")
        for entry in memory_store.entries:
            with st.expander(f"[{entry.category}] {entry.title} ({entry.timestamp})"):
                st.write(entry.content)
                st.caption(f"Tags: {', '.join(entry.tags)} | Related: {', '.join(entry.related_tasks)}")
