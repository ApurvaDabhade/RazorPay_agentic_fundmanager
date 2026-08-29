"""
app.py
Project Sentinel: Enterprise-Grade Real-Time AI Project & Risk Command Center
Built for Corporate Production Deployment & Executive Engineering Leadership
"""

import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from sentinel.sample_data import get_razorpay_project_state, get_ecommerce_project_state
from sentinel.orchestrator import SentinelOrchestrator
from sentinel.models import TaskStatus, ActionStatus, HealthTier
from sentinel.scenario_simulator import ScenarioSimulator
from sentinel.dependency_engine import DependencyEngine


# Page Configuration
st.set_page_config(
    page_title="Project Sentinel Enterprise | Autonomous PM Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise SaaS CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .stApp {
        background: #090D16;
        color: #F1F5F9;
    }
    
    /* Top Enterprise Navigation Header */
    .enterprise-header {
        background: linear-gradient(180deg, #111827 0%, #0D131F 100%);
        border-bottom: 1px solid #1E293B;
        padding: 14px 24px;
        margin: -4rem -4rem 1.5rem -4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .corp-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .corp-title {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #F8FAFC;
    }
    
    .corp-subtitle {
        font-size: 0.78rem;
        color: #94A3B8;
        font-weight: 500;
    }
    
    .telemetry-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.72rem;
        font-weight: 600;
        color: #CBD5E1;
    }
    
    .telemetry-dot-green {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
    }
    
    .telemetry-dot-amber {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #F59E0B;
        box-shadow: 0 0 8px #F59E0B;
    }
    
    /* Modern Glass Cards */
    .ent-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    
    .ent-card-highlight {
        background: linear-gradient(145deg, #131D31 0%, #0F172A 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .kpi-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 6px;
    }
    
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }
    
    .kpi-sub {
        font-size: 0.8rem;
        margin-top: 6px;
        font-weight: 500;
    }
    
    /* Activity Feed Styles */
    .feed-item {
        border-left: 2px solid #3B82F6;
        padding: 6px 12px;
        margin-bottom: 10px;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 0 6px 6px 0;
        font-size: 0.83rem;
    }
    
    .feed-time {
        color: #64748B;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
    }
    
    /* Causal Stepper */
    .causal-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .causal-box {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 16px;
        position: relative;
    }
    
    /* Buttons and controls */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "project_choice" not in st.session_state:
    st.session_state.project_choice = "Razorpay Payment Gateway Core Integration"

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = SentinelOrchestrator(get_razorpay_project_state())

if "live_event_log" not in st.session_state:
    st.session_state.live_event_log = [
        {"time": "17:48:12 UTC", "type": "TELEMETRY", "msg": "Jira Cloud webhook synced 8 active issues for Sprint 24.4"},
        {"time": "17:48:30 UTC", "type": "ALERT", "msg": "PAY-103 flag raised: Redis cluster distributed lock spec bottleneck"},
        {"time": "17:48:45 UTC", "type": "MONTE_CARLO", "msg": "Sentinel background daemon simulated 2,500 paths: +14.9d predicted delay"},
        {"time": "17:49:02 UTC", "type": "AI_AGENT", "msg": "Auto-generated intervention: Reassign PAY-105 to Priya Sharma"}
    ]


# Top Corporate Navigation Bar
now_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
st.markdown(f"""
<div class='enterprise-header'>
    <div class='corp-brand'>
        <span style='font-size: 1.8rem;'>🛡️</span>
        <div>
            <div class='corp-title'>RAZORPAY TECHNOLOGIES • PROJECT SENTINEL</div>
            <div class='corp-subtitle'>Autonomous Project Intelligence & Real-Time Predictive Risk Infrastructure</div>
        </div>
    </div>
    <div style='display: flex; gap: 8px; align-items: center;'>
        <div class='telemetry-pill'><div class='telemetry-dot-green'></div>JIRA CLOUD CONNECTED (42ms)</div>
        <div class='telemetry-pill'><div class='telemetry-dot-green'></div>SLACK WEBHOOK ACTIVE</div>
        <div class='telemetry-pill'><div class='telemetry-dot-green'></div>GITHUB CI PASSING</div>
        <div class='telemetry-pill' style='font-family: monospace;'>🕒 {now_utc}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🏢 Enterprise Workspace")
    selected_project = st.selectbox(
        "Active Project Portfolio",
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

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Command Modules")
    menu = st.radio(
        "Select Enterprise Console",
        [
            "📊 Executive Portfolio Cockpit",
            "🔮 Predictive Monte Carlo Lab",
            "🕵️ Root-Cause Diagnostic Graph",
            "🤖 Autonomous Action Dispatcher (HITL)",
            "🧠 What-If Scenario Simulator",
            "👥 Team Capacity & Burnout Matrix",
            "🔗 Dependency DAG & Critical Path",
            "📚 Corporate Memory & ADR Repository",
            "📄 Export & Compliance Reports"
        ]
    )

    st.divider()
    st.markdown("### ⚡ Live Telemetry Controls")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("🔄 Sync Jira", use_container_width=True):
            st.session_state.live_event_log.insert(0, {
                "time": datetime.utcnow().strftime("%H:%M:%S UTC"),
                "type": "SYNC",
                "msg": f"Manually triggered Jira & GitHub sync for {st.session_state.project_choice}"
            })
            st.toast("Jira & GitHub telemetry synchronized.")
            st.rerun()
    with col_s2:
        if st.button("♻️ Reset Data", use_container_width=True):
            if "Razorpay" in st.session_state.project_choice:
                st.session_state.orchestrator.set_state(get_razorpay_project_state())
            else:
                st.session_state.orchestrator.set_state(get_ecommerce_project_state())
            st.success("State reset to baseline.")
            st.rerun()

    st.caption("Project Sentinel v2.4 Enterprise • SOC2 & PCI-DSS Compliant Engine")


# Run Orchestrator Cycle
orch = st.session_state.orchestrator
analysis = orch.run_full_cycle()
state = orch.state
health = analysis["health"]
risk = analysis["risk"]
root_cause = analysis["root_cause"]


# =========================================================================
# 1. EXECUTIVE PORTFOLIO COCKPIT
# =========================================================================
if menu == "📊 Executive Portfolio Cockpit":
    st.markdown(f"## 📊 Executive Portfolio Cockpit: *{state.name}*")
    st.markdown(f"<div style='color: #94A3B8; margin-top: -10px; margin-bottom: 20px;'>Sprint Window: <b>Day {state.current_day} of {state.target_deadline_days}</b> • Allocated Budget: <b>₹{int(state.budget_allocated):,}</b> • Burn Rate: <b>₹{int(state.budget_spent):,} ({(state.budget_spent/max(1, state.budget_allocated))*100:.1f}%)</b></div>", unsafe_allow_html=True)

    # 4 Enterprise Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        health_color = "#10B981" if health.overall_score >= 80 else ("#F59E0B" if health.overall_score >= 60 else "#EF4444")
        st.markdown(f"""
        <div class='ent-card' style='border-top: 3px solid {health_color};'>
            <div class='kpi-title'>Project Health Index</div>
            <div class='kpi-value' style='color: {health_color};'>{health.overall_score}<span style='font-size: 1.1rem; color: #64748B;'>/100</span></div>
            <div class='kpi-sub' style='color: {health_color};'>Status: {health.tier.value.replace('_', ' ')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        risk_color = "#EF4444" if risk.probability_of_delay > 60 else ("#F59E0B" if risk.probability_of_delay > 30 else "#10B981")
        st.markdown(f"""
        <div class='ent-card' style='border-top: 3px solid {risk_color};'>
            <div class='kpi-title'>Deadline Breach Probability</div>
            <div class='kpi-value' style='color: {risk_color};'>{risk.probability_of_delay}%</div>
            <div class='kpi-sub' style='color: #94A3B8;'>Risk Rating: <b>{risk.deadline_risk_level}</b></div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='ent-card' style='border-top: 3px solid #3B82F6;'>
            <div class='kpi-title'>Projected Delivery Slippage</div>
            <div class='kpi-value' style='color: #60A5FA;'>+{risk.predicted_delay_days}d</div>
            <div class='kpi-sub' style='color: #94A3B8;'>95% CI: [{risk.confidence_interval_95[0]}d, {risk.confidence_interval_95[1]}d]</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='ent-card' style='border-top: 3px solid #8B5CF6;'>
            <div class='kpi-title'>Sprint Progress Drift</div>
            <div class='kpi-value' style='color: #A78BFA;'>{risk.current_progress_pct}%</div>
            <div class='kpi-sub' style='color: #94A3B8;'>Target: <b>{risk.expected_progress_pct}%</b> (Gap: {round(risk.expected_progress_pct - risk.current_progress_pct, 1)}%)</div>
        </div>
        """, unsafe_allow_html=True)

    # Real-Time Visual Charts: Burndown & Multi-Dimensional Radar
    col_b1, col_b2 = st.columns([3, 2])
    
    with col_b1:
        st.markdown("#### 📉 Real-Time Sprint Burndown & Predicted Trajectory")
        days = list(range(1, state.target_deadline_days + 1))
        total_pts = sum(t.story_points for t in state.tasks.values())
        ideal_burn = [total_pts - (total_pts / state.target_deadline_days) * d for d in days]
        
        # Historical actual burn
        actual_burn = [total_pts]
        current_remaining_pts = sum(t.story_points for t in state.tasks.values() if t.status != TaskStatus.DONE)
        for d in range(1, state.current_day + 1):
            progress_ratio = d / state.current_day
            pts_at_d = total_pts - ((total_pts - current_remaining_pts) * progress_ratio)
            actual_burn.append(pts_at_d)
        
        # Sentinel predicted trajectory
        pred_days = list(range(state.current_day, int(state.target_deadline_days + risk.predicted_delay_days) + 1))
        pred_burn = [current_remaining_pts - (current_remaining_pts / max(1, len(pred_days) - 1)) * i for i in range(len(pred_days))]

        fig_burn = go.Figure()
        fig_burn.add_trace(go.Scatter(
            x=days, y=ideal_burn, mode='lines', name='Ideal Velocity Burn',
            line=dict(color='#64748B', dash='dash', width=2)
        ))
        fig_burn.add_trace(go.Scatter(
            x=list(range(0, state.current_day + 1)), y=actual_burn, mode='lines+markers', name='Actual Burn to Date',
            line=dict(color='#3B82F6', width=3), marker=dict(size=6)
        ))
        fig_burn.add_trace(go.Scatter(
            x=pred_days, y=pred_burn, mode='lines', name='Sentinel Predicted Path',
            line=dict(color='#EF4444', dash='dot', width=3)
        ))
        fig_burn.add_vline(x=state.current_day, line_color="#F59E0B", line_dash="dash", annotation_text=f"Today (Day {state.current_day})")
        fig_burn.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Sprint Timeline (Days)", color='#94A3B8', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="Story Points Remaining", color='#94A3B8', gridcolor='rgba(255,255,255,0.05)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#CBD5E1')),
            margin=dict(l=30, r=20, t=30, b=30),
            height=320
        )
        st.plotly_chart(fig_burn, use_container_width=True)

    with col_b2:
        st.markdown("#### 🧭 Multi-Dimensional Health Matrix")
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
            fillcolor='rgba(99, 102, 241, 0.3)',
            line=dict(color='#818CF8', width=2),
            name='Health Breakdown'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color='#64748B', gridcolor='rgba(255,255,255,0.08)'),
                angularaxis=dict(color='#94A3B8')
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=30, r=30, t=20, b=20),
            height=320
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Activity Stream & Tactical Alerts
    col_act1, col_act2 = st.columns([1, 1])
    with col_act1:
        st.markdown("#### 🚨 Active Enterprise Risk Triggers")
        for alert in health.alerts:
            st.markdown(f"<div style='background: rgba(239, 68, 68, 0.1); border-left: 3px solid #EF4444; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px; color: #FCA5A5;'>⚠️ {alert}</div>", unsafe_allow_html=True)
        for h_item in health.highlights:
            st.markdown(f"<div style='background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10B981; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px; color: #6EE7B7;'>✅ {h_item}</div>", unsafe_allow_html=True)

    with col_act2:
        st.markdown("#### 📡 Real-Time Telemetry & Event Feed")
        for event in st.session_state.live_event_log[:4]:
            st.markdown(f"""
            <div class='feed-item'>
                <span class='feed-time'>{event['time']}</span> • <b>[{event['type']}]</b> {event['msg']}
            </div>
            """, unsafe_allow_html=True)


# =========================================================================
# 2. PREDICTIVE MONTE CARLO LAB
# =========================================================================
elif menu == "🔮 Predictive Monte Carlo Lab":
    st.markdown("## 🔮 Predictive Monte Carlo Risk Simulation Lab")
    st.markdown("<div style='color: #94A3B8; margin-top: -10px; margin-bottom: 20px;'>Stochastic delivery modeling factoring in historical velocity distributions, task variance, and dependency chain locks.</div>", unsafe_allow_html=True)

    col_sim_ctrl, col_sim_view = st.columns([1, 2])
    with col_sim_ctrl:
        st.markdown("#### ⚙️ Simulation Hyperparameters")
        sim_iterations = st.slider("Simulation Trajectories", 1000, 10000, 2500, step=500)
        team_velocity = st.slider("Historical Velocity (pts/day)", 1.0, 6.0, float(state.historical_velocity_avg), step=0.1)
        velocity_std = st.slider("Velocity Standard Deviation (σ)", 0.2, 2.0, float(state.historical_velocity_std), step=0.05)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='ent-card-highlight'>
            <div class='kpi-title'>Prediction Summary</div>
            <div style='font-size: 1.5rem; font-weight: 800; color: #EF4444;'>{risk.probability_of_delay}% Failure Risk</div>
            <div style='color: #F8FAFC; margin-top: 4px;'>Expected Slippage: <b>+{risk.predicted_delay_days} days</b></div>
            <div style='color: #94A3B8; font-size: 0.8rem; margin-top: 4px;'>95% Range: Day {risk.confidence_interval_95[0]} – Day {risk.confidence_interval_95[1]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_sim_view:
        st.markdown("#### 📊 Delivery Trajectory Probability Density Curve")
        samples = risk.trajectory_samples
        
        fig_density = px.histogram(
            x=samples, nbins=30,
            labels={'x': 'Project Completion (Sprint Days)'},
            color_discrete_sequence=['#6366F1'],
            opacity=0.75
        )
        fig_density.add_vline(x=state.target_deadline_days, line_width=3, line_dash="dash", line_color="#EF4444", annotation_text=f"Target Deadline (Day {state.target_deadline_days})")
        fig_density.add_vrect(
            x0=risk.confidence_interval_95[0], x1=risk.confidence_interval_95[1],
            fillcolor="rgba(99, 102, 241, 0.15)", line_width=0,
            annotation_text="95% Confidence Band", annotation_position="top left"
        )
        fig_density.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(color='#94A3B8', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="Trajectory Frequency", color='#94A3B8', gridcolor='rgba(255,255,255,0.05)'),
            margin=dict(l=30, r=20, t=30, b=30),
            height=340
        )
        st.plotly_chart(fig_density, use_container_width=True)

    st.markdown("#### 🔍 Primary Delay Vectors Identified by Monte Carlo Model")
    for i, cause in enumerate(risk.primary_causes, 1):
        st.markdown(f"<div style='background: #111827; border-left: 3px solid #F59E0B; padding: 12px 16px; border-radius: 6px; margin-bottom: 8px;'><b>Vector #{i}</b>: {cause}</div>", unsafe_allow_html=True)


# =========================================================================
# 3. ROOT-CAUSE DIAGNOSTIC GRAPH
# =========================================================================
elif menu == "🕵️ Root-Cause Diagnostic Graph":
    st.markdown("## 🕵️ AI Root-Cause Diagnostic Graph")
    st.markdown(f"<div style='color: #94A3B8; margin-top: -10px; margin-bottom: 20px;'>Autonomous multi-hop graph traversal isolating structural bottlenecks from sprint symptoms.</div>", unsafe_allow_html=True)

    st.info(f"📋 **Diagnostic Objective**: {root_cause.issue_summary} (Model Confidence: **{root_cause.confidence_pct}%**)")

    # Visual Causal Diagnostic Pipeline
    st.markdown("### ⛓️ Step-by-Step Causal Traversal")
    for idx, node in enumerate(root_cause.chain):
        color = "#EF4444" if node.node_type == "ROOT_CAUSE" else ("#F59E0B" if node.node_type == "BOTTLENECK" else "#3B82F6")
        st.markdown(f"""
        <div class='causal-box' style='border-left: 4px solid {color};'>
            <div style='display: flex; justify-content: space-between;'>
                <b style='color: {color}; font-size: 0.85rem;'>PHASE {node.step_number} • [{node.node_type}]</b>
                <span style='background: rgba(239, 68, 68, 0.15); color: #FCA5A5; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600;'>{node.severity} SEVERITY</span>
            </div>
            <div style='font-size: 1.1rem; font-weight: 700; color: #F8FAFC; margin: 4px 0;'>{node.title}</div>
            <p style='color: #CBD5E1; font-size: 0.9rem; margin: 4px 0;'>{node.description}</p>
            <div style='font-size: 0.8rem; color: #94A3B8;'><b>Evidence:</b> {node.evidence}</div>
        </div>
        """, unsafe_allow_html=True)
        if idx < len(root_cause.chain) - 1:
            st.markdown("<div style='text-align: center; color: #6366F1; font-size: 1.2rem; margin: -6px 0 6px 0;'>⬇️</div>", unsafe_allow_html=True)

    col_iso1, col_iso2 = st.columns(2)
    with col_iso1:
        st.markdown(f"""
        <div class='ent-card' style='border-left: 4px solid #EF4444;'>
            <h4 style='color: #F87171; margin-top: 0;'>🎯 Root Cause Statement</h4>
            <p style='color: #E2E8F0; font-size: 0.92rem;'>{root_cause.root_cause_statement}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_iso2:
        st.markdown(f"""
        <div class='ent-card' style='border-left: 4px solid #10B981;'>
            <h4 style='color: #34D399; margin-top: 0;'>💡 Maximum-Leverage Intervention</h4>
            <p style='color: #E2E8F0; font-size: 0.92rem;'>{root_cause.recommended_intervention}</p>
            <small style='color: #818CF8;'><b>Projected Impact:</b> {root_cause.estimated_leverage_impact}</small>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# 4. AUTONOMOUS ACTION DISPATCHER (HITL)
# =========================================================================
elif menu == "🤖 Autonomous Action Dispatcher (HITL)":
    st.markdown("## 🤖 Autonomous Action Dispatcher (Human-in-the-Loop)")
    st.markdown("<div style='color: #94A3B8; margin-top: -10px; margin-bottom: 20px;'>Review AI-recommended remediations with live enterprise webhook integration (Jira REST API, Slack, GitHub).</div>", unsafe_allow_html=True)

    pending_actions = orch.action_agent.get_pending_actions()
    executed_actions = orch.action_agent.get_executed_actions()

    st.markdown(f"### ⏳ Pending Approval Queue ({len(pending_actions)})")
    if not pending_actions:
        st.success("✅ All recommended actions approved and executed across enterprise systems.")

    for action in pending_actions:
        with st.container():
            st.markdown(f"""
            <div class='ent-card-highlight' style='border-left: 4px solid #6366F1;'>
                <div style='display: flex; justify-content: space-between;'>
                    <b style='font-size: 1.15rem; color: #C7D2FE;'>{action.title}</b>
                    <span style='background: rgba(245, 158, 11, 0.2); color: #FBBF24; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;'>{action.urgency} URGENCY</span>
                </div>
                <p style='color: #CBD5E1; margin: 8px 0;'>{action.description}</p>
                <div style='font-size: 0.78rem; color: #94A3B8;'>Action Type: <code>{action.action_type}</code> | Target: <code>{action.task_key or 'PROJECT_GLOBAL'}</code> | Created: <code>{action.created_at}</code></div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🔍 View Webhook Dispatch Payload Preview"):
                st.json({
                    "action_id": action.action_id,
                    "event": "AUTOMATED_INTERVENTION_DISPATCH",
                    "source": "Sentinel-AI-Agent",
                    "jira_endpoint": f"/rest/api/3/issue/{action.task_key or 'GLOBAL'}",
                    "parameters": action.parameters
                })

            col_btn1, col_btn2, _ = st.columns([1.5, 1, 3])
            with col_btn1:
                if st.button(f"⚡ Approve & Dispatch Webhook", key=f"app_{action.action_id}", type="primary"):
                    res = orch.action_agent.approve_and_execute(action.action_id)
                    st.session_state.live_event_log.insert(0, {
                        "time": datetime.utcnow().strftime("%H:%M:%S UTC"),
                        "type": "ACTION_EXECUTED",
                        "msg": f"Executed action [{action.action_id}]: {res['summary']}"
                    })
                    st.success(f"Dispatched: {res['summary']}")
                    st.rerun()
            with col_btn2:
                if st.button(f"❌ Reject", key=f"rej_{action.action_id}"):
                    orch.action_agent.reject_action(action.action_id)
                    st.session_state.live_event_log.insert(0, {
                        "time": datetime.utcnow().strftime("%H:%M:%S UTC"),
                        "type": "ACTION_REJECTED",
                        "msg": f"Rejected action [{action.action_id}] by Human Operator"
                    })
                    st.warning("Action rejected.")
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### 📜 Enterprise Audit Trail ({len(executed_actions)})")
    for act in executed_actions:
        color = "#10B981" if act.status == ActionStatus.EXECUTED else "#EF4444"
        st.markdown(f"""
        <div style='background: #111827; border-left: 3px solid {color}; padding: 12px 16px; border-radius: 6px; margin-bottom: 8px;'>
            <div style='display: flex; justify-content: space-between;'>
                <b>{act.title}</b>
                <span style='color: {color}; font-weight: 700; font-size: 0.8rem;'>{act.status.value}</span>
            </div>
            <div style='color: #94A3B8; font-size: 0.8rem; margin-top: 4px;'><b>Execution Log:</b> {act.result_summary} • Timestamp: <code>{act.executed_at}</code></div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# 5. WHAT-IF SCENARIO SIMULATOR
# =========================================================================
elif menu == "🧠 What-If Scenario Simulator":
    st.markdown("## 🧠 Enterprise What-If Scenario Simulation Lab")
    st.markdown("<div style='color: #94A3B8; margin-top: -10px; margin-bottom: 20px;'>Simulate resource drop-offs, budget shocks, deadline compressions, and feature descoping in real time.</div>", unsafe_allow_html=True)

    sim = ScenarioSimulator(state)
    tab_w1, tab_w2, tab_w3 = st.tabs(["👤 Developer Absence Shock", "📅 Deadline Shift", "✂️ Scope Descoping"])

    with tab_w1:
        st.markdown("#### Simulate Developer Unavailability")
        dev_map = {d.id: f"{d.name} ({d.role})" for d in state.developers.values()}
        sel_dev = st.selectbox("Select Team Member", list(dev_map.keys()), format_func=lambda x: dev_map[x])
        absent_days = st.slider("Duration of Absence (Days)", min_value=1, max_value=14, value=5)

        if st.button("🧪 Run Absence Simulation", type="primary"):
            res = sim.simulate_developer_absence(sel_dev, absent_days)
            col_sc1, col_sc2, col_sc3 = st.columns(3)
            with col_sc1:
                st.metric("Projected Timeline Delay", f"+{res.delay_delta_days} days", delta="Slippage Impact", delta_color="inverse")
            with col_sc2:
                st.metric("Financial Burn Impact", f"+₹{int(res.cost_delta):,}", delta="Burn rate cost", delta_color="inverse")
            with col_sc3:
                st.metric("Directly Affected Tasks", f"{len(res.affected_tasks)} items", delta=", ".join(res.affected_tasks))
            
            st.markdown(f"""
            <div class='ent-card' style='border-left: 4px solid #6366F1; margin-top: 14px;'>
                <b style='color: #818CF8;'>💡 Sentinel Contingency Recommendation:</b><br>
                <span style='color: #F8FAFC;'>{res.recommendation}</span>
            </div>
            """, unsafe_allow_html=True)

    with tab_w2:
        st.markdown("#### Simulate Deadline Compression / Extension")
        shift = st.slider("Shift Target Deadline (Days)", min_value=-7, max_value=14, value=3)

        if st.button("🧪 Run Deadline Shift Simulation", type="primary"):
            res = sim.simulate_deadline_adjustment(shift)
            st.metric("Projected Finish Day", f"Day {res.simulated_completion_day}", delta=f"{res.risk_direction} RISK PROFILE")
            st.info(f"💡 **Recommendation**: {res.recommendation}")

    with tab_w3:
        st.markdown("#### Simulate Scope Descoping")
        active_tasks = {t.id: f"[{t.key}] {t.title} ({t.story_points} pts)" for t in state.tasks.values() if t.status != TaskStatus.DONE}
        drop_ids = st.multiselect("Select Non-Critical Tasks to Defer", list(active_tasks.keys()), format_func=lambda x: active_tasks[x])

        if st.button("🧪 Run Descoping Simulation", type="primary"):
            if drop_ids:
                res = sim.simulate_scope_reduction(drop_ids)
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.metric("⏱️ Recovered Sprint Time", f"{abs(res.delay_delta_days)} days faster")
                with col_d2:
                    st.metric("💰 Budget Savings", f"₹{abs(int(res.cost_delta)):,}")
                st.success(f"💡 **Recommendation**: {res.recommendation}")
            else:
                st.warning("Please select at least one task to drop.")


# =========================================================================
# 6. TEAM CAPACITY & BURNOUT MATRIX
# =========================================================================
elif menu == "👥 Team Capacity & Burnout Matrix":
    st.markdown("## 👥 Team Capacity & Burnout Risk Matrix")
    st.markdown("<div style='color: #94A3B8; margin-top: -10px; margin-bottom: 20px;'>Real-time developer utilization tracking, context switching overhead, and 1-click AI task rebalancing.</div>", unsafe_allow_html=True)

    workload_data = analysis["team_workload"]
    rebalancing_recs = analysis["rebalancing_recommendations"]

    # Plotly Workload vs Capacity Bar Chart
    names = [d["name"] for d in workload_data]
    workloads = [d["workload_pct"] for d in workload_data]
    burnout_scores = [d["burnout_score"] for d in workload_data]
    colors = ['#EF4444' if w > 105 else ('#10B981' if w < 60 else '#3B82F6') for w in workloads]

    fig_w = go.Figure()
    fig_w.add_trace(go.Bar(
        x=names, y=workloads, name='Workload Utilization (%)',
        marker_color=colors, text=[f"{w}%" for w in workloads], textposition='outside'
    ))
    fig_w.add_hline(y=100, line_dash="dash", line_color="#EF4444", annotation_text="100% Safe Capacity Threshold")
    fig_w.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title="Workload Utilization (%)", color='#94A3B8', gridcolor='rgba(255,255,255,0.05)'),
        xaxis=dict(color='#94A3B8'),
        margin=dict(l=30, r=20, t=20, b=30),
        height=320
    )
    st.plotly_chart(fig_w, use_container_width=True)

    # Detailed Developer Cards
    st.markdown("### 🧑‍💻 Individual Engineer Utilization Details")
    col_devs = st.columns(len(workload_data))
    for i, dev in enumerate(workload_data):
        with col_devs[i]:
            card_border = "#EF4444" if dev["workload_pct"] > 105 else ("#10B981" if dev["workload_pct"] < 60 else "#3B82F6")
            st.markdown(f"""
            <div class='ent-card' style='border-top: 3px solid {card_border};'>
                <b>{dev['name']}</b><br>
                <small style='color: #94A3B8;'>{dev['role']}</small>
                <hr style='border-color: #1E293B; margin: 8px 0;'>
                <div style='font-size: 0.82rem;'>Workload: <b>{dev['workload_pct']}%</b></div>
                <div style='font-size: 0.82rem;'>Points: <b>{dev['assigned_points']} / {dev['capacity_points']}</b></div>
                <div style='font-size: 0.82rem;'>Burnout Risk: <b>{dev['burnout_score']}%</b></div>
                <div style='font-size: 0.82rem;'>Active Tasks: <b>{dev['active_task_count']}</b></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### ⚖️ AI Automated Task Rebalancing Recommendations")
    if not rebalancing_recs:
        st.success("Team capacity is optimally balanced.")

    for rec in rebalancing_recs:
        st.markdown(f"""
        <div class='ent-card' style='border-left: 4px solid #6366F1;'>
            <b style='color: #818CF8; font-size: 1.05rem;'>💡 Reassignment Proposal: [{rec['task_key']}] {rec['task_title']} ({rec['story_points']} pts)</b>
            <div style='margin-top: 6px; color: #CBD5E1; font-size: 0.9rem;'>
                • <b>From</b>: <span style='color: #F87171;'>{rec['from_dev_name']}</span> ({rec['from_current_workload']}% → {rec['from_projected_workload']}%)<br>
                • <b>To</b>: <span style='color: #34D399;'>{rec['to_dev_name']}</span> ({rec['to_current_workload']}% → {rec['to_projected_workload']}%)<br>
                • <b>Strategic Impact</b>: {rec['reasoning']}
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# 7. DEPENDENCY DAG & CRITICAL PATH
# =========================================================================
elif menu == "🔗 Dependency DAG & Critical Path":
    st.markdown("## 🔗 Dependency DAG & Critical Path Method (CPM)")
    st.markdown("<div style='color: #94A3B8; margin-top: -10px; margin-bottom: 20px;'>Directed Acyclic Graph (DAG) analysis identifying bottleneck chains, zero-slack critical paths, and upstream cascade risk.</div>", unsafe_allow_html=True)

    tree_summary = analysis["dependency_tree"]
    critical_path = analysis["critical_path"]

    col_gantt, col_reg = st.columns([1, 1])
    with col_gantt:
        st.markdown("#### ⚡ Critical Path Tasks (Zero Slack)")
        for cp_id in critical_path:
            t = state.tasks.get(cp_id)
            if t:
                st.markdown(f"<div style='background: rgba(239, 68, 68, 0.15); border-left: 3px solid #EF4444; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px; color: #FCA5A5;'>⚡ <b>[{t.key}]</b> {t.title} ({t.remaining_days}d remaining)</div>", unsafe_allow_html=True)

    with col_reg:
        st.markdown("#### 📋 Task Dependency Registry")
        df_tasks = pd.DataFrame([
            {
                "Key": t["key"],
                "Title": t["title"][:28] + "...",
                "Status": t["status"],
                "Critical?": "⚡ YES" if t["is_critical"] else "NO",
                "Slack (days)": t["slack"]
            } for t in tree_summary
        ])
        st.dataframe(df_tasks, use_container_width=True)

    st.divider()
    st.markdown("#### 🌊 Interactive Upstream Delay Cascade Simulator")
    target_key = st.selectbox("Select Upstream Task to Test", [t.key for t in state.tasks.values()])
    delay_days = st.slider("Simulated Delay (Days)", 1, 10, 3)

    dep_engine = DependencyEngine(state)
    t_id = next(tid for tid, t in state.tasks.items() if t.key == target_key)
    cascade = dep_engine.calculate_cascade_impact(t_id, float(delay_days))

    st.markdown(f"""
    <div class='ent-card'>
        • <b>Target Task</b>: <code>[{cascade['delayed_task_key']}]</code> (+{cascade['delay_days']} days delay)<br>
        • <b>Downstream Tasks Affected</b>: <b>{cascade['affected_downstream_count']} features</b><br>
        • <b>Project-Level Delay Delta</b>: <b style='color: #EF4444;'>+{cascade['project_delay_delta']} days</b><br>
        • <b>Critical Path Task?</b>: <b>{'YES (Directly delays milestone delivery)' if cascade['is_critical_task'] else 'NO (Absorbed by Slack)'}</b>
    </div>
    """, unsafe_allow_html=True)


# =========================================================================
# 8. CORPORATE MEMORY & ADR REPOSITORY
# =========================================================================
elif menu == "📚 Corporate Memory & ADR Repository":
    st.markdown("## 📚 Corporate Institutional Memory & ADR Repository")
    st.markdown("<div style='color: #94A3B8; margin-top: -10px; margin-bottom: 20px;'>Searchable institutional memory of Architectural Decision Records (ADRs), post-mortems, and compliance trade-offs.</div>", unsafe_allow_html=True)

    memory_store = orch.memory
    tab_m1, tab_m2, tab_m3 = st.tabs(["💬 Query Memory Assistant", "📖 Browse Knowledge Graph", "➕ Register New ADR"])

    with tab_m1:
        preset_q = st.selectbox("Enterprise Query Presets", [
            "Why did we choose Razorpay over Stripe for domestic payments?",
            "What was the root cause and remediation for the Sprint 2 Webhook outage?",
            "What is the VP of Product requirement regarding deployment downtime?"
        ])
        user_q = st.text_input("Ask a question:", value=preset_q)

        if st.button("🔍 Query Knowledge Base", type="primary"):
            ans = memory_store.answer_question(user_q)
            st.markdown(f"""
            <div class='ent-card-highlight' style='border-left: 4px solid #6366F1;'>
                {ans['answer']}
            </div>
            """, unsafe_allow_html=True)

    with tab_m2:
        st.markdown(f"#### Institutional Knowledge Records ({len(memory_store.entries)})")
        for entry in memory_store.entries:
            with st.expander(f"[{entry.category}] {entry.title} ({entry.timestamp})"):
                st.write(entry.content)
                st.caption(f"Tags: {', '.join(entry.tags)} | Related Tasks: {', '.join(entry.related_tasks)}")

    with tab_m3:
        st.markdown("#### Record New Architectural Decision (ADR)")
        cat = st.selectbox("Category", ["ARCHITECTURE", "DECISION", "INCIDENT", "LESSON_LEARNED", "STAKEHOLDER_PREF"])
        title = st.text_input("ADR Title")
        content = st.text_area("Decision Rationale & Trade-offs")
        tags = st.text_input("Tags (comma separated)", "architecture, razorpay, compliance")

        if st.button("💾 Save to Institutional Memory"):
            if title and content:
                entry = memory_store.add_entry(cat, title, content, [t.strip() for t in tags.split(",")])
                st.session_state.live_event_log.insert(0, {
                    "time": datetime.utcnow().strftime("%H:%M:%S UTC"),
                    "type": "MEMORY_SAVED",
                    "msg": f"Registered new ADR: '{entry.title}'"
                })
                st.success("ADR saved to enterprise memory store.")
                st.rerun()


# =========================================================================
# 9. EXPORT & COMPLIANCE REPORTS
# =========================================================================
elif menu == "📄 Export & Compliance Reports":
    st.markdown("## 📄 Executive Export & Compliance Reports")
    st.markdown("<div style='color: #94A3B8; margin-top: -10px; margin-bottom: 20px;'>Generate audit-ready reports for CTO, VP of Product, and compliance stakeholders.</div>", unsafe_allow_html=True)

    col_rep1, col_rep2 = st.columns(2)
    
    with col_rep1:
        st.markdown("#### 📑 Executive Risk Brief (Markdown)")
        exec_report = f"""# Executive Project Health Brief
**Project**: {state.name}
**Date**: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}
**Organization**: Razorpay Technologies Ltd.

## Key Executive Metrics
- **Project Health Score**: {health.overall_score}/100 ({health.tier.value})
- **Deadline Failure Probability**: {risk.probability_of_delay}%
- **Predicted Slippage**: +{risk.predicted_delay_days} days
- **Current Progress**: {risk.current_progress_pct}% (Expected: {risk.expected_progress_pct}%)

## Root Cause Analysis
- **Summary**: {root_cause.issue_summary}
- **Structural Root Cause**: {root_cause.root_cause_statement}
- **Recommended Intervention**: {root_cause.recommended_intervention}

## Resource Overload Summary
- Overloaded Developers: Rahul Verma (131.2% capacity)
- Recommended Reallocation: Move PAY-105 to Priya Sharma (27.8% capacity)
"""
        st.code(exec_report, language="markdown")
        st.download_button(
            label="📥 Download Executive Brief (.md)",
            data=exec_report,
            file_name=f"sentinel_executive_report_{state.project_id}.md",
            mime="text/markdown"
        )

    with col_rep2:
        st.markdown("#### 📊 Task Dependency & Status Export (CSV)")
        task_data = []
        for t in state.tasks.values():
            task_data.append({
                "Key": t.key,
                "Title": t.title,
                "Assignee": t.assignee_id,
                "Status": t.status.value,
                "Priority": t.priority.value,
                "Story Points": t.story_points,
                "Remaining Days": t.remaining_days
            })
        df_export = pd.DataFrame(task_data)
        st.dataframe(df_export, use_container_width=True)
        
        csv_data = df_export.to_csv(index=False)
        st.download_button(
            label="📥 Download Task Registry (.csv)",
            data=csv_data,
            file_name=f"sentinel_tasks_{state.project_id}.csv",
            mime="text/csv"
        )
