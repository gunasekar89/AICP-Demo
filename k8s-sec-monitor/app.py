"""Streamlit dashboard for the AI-SecOps Kubernetes security monitor."""
from __future__ import annotations

import json
import random
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Ensure local package imports take precedence over repo-level modules.
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from agents.simulator import ThreatEvent, generate_event
from core.correlation import detect_chain, predict_next_stage, score_threat
from core.response import auto_quarantine, execute_playbook, generate_patch_recommendation
from ml.analyzer import RiskAnalyzer

DATA_PATH = CURRENT_DIR / "data" / "sample_events.json"
MAX_EVENTS = 250
REFRESH_INTERVAL_MS = 5000


st.set_page_config(
    page_title="AI-SecOps: Autonomous Kubernetes Defense",
    page_icon="🛡️",
    layout="wide",
)

def _load_initial_events() -> List[Dict]:
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return raw
    # fallback to generated events
    return [asdict(generate_event()) for _ in range(40)]


def _ensure_state() -> None:
    if "events" not in st.session_state:
        st.session_state.events = _load_initial_events()
    if "response_log" not in st.session_state:
        st.session_state.response_log = []


def _append_event(event: ThreatEvent) -> None:
    records = st.session_state.events
    records.append(asdict(event))
    st.session_state.events = records[-MAX_EVENTS:]


def _refresh_events() -> None:
    burst = random.random() < 0.3
    count = random.randint(1, 4) if burst else 1
    for _ in range(count):
        _append_event(generate_event())


def _event_dataframe(events: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(events)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["risk_score"] = df.apply(score_threat, axis=1)
    return df


def _cluster_map(df: pd.DataFrame) -> go.Figure:
    clusters = df.groupby("cluster").agg({"risk_score": "mean", "severity": "count"}).reset_index()
    coords = {
        "prod-east-1": (1, 4),
        "prod-west-2": (-2, 3),
        "staging-eu-1": (0, 0),
        "dev-apac-2": (3, -2),
    }
    clusters["x"] = clusters["cluster"].map(lambda c: coords.get(c, (random.random(), random.random()))[0])
    clusters["y"] = clusters["cluster"].map(lambda c: coords.get(c, (random.random(), random.random()))[1])

    fig = px.scatter(
        clusters,
        x="x",
        y="y",
        size="severity",
        color="risk_score",
        color_continuous_scale="Reds",
        hover_data={"cluster": True, "risk_score": True, "severity": True, "x": False, "y": False},
    )
    fig.update_layout(
        title="Cluster Threat Landscape",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="#fafafa"),
    )
    fig.update_traces(marker=dict(line=dict(width=2, color="#222")))
    return fig


def _risk_heatmap(df: pd.DataFrame) -> go.Figure:
    heatmap = df.groupby(["node", "namespace"])["risk_score"].mean().reset_index()
    pivot = heatmap.pivot(index="node", columns="namespace", values="risk_score").fillna(0)
    fig = px.imshow(
        pivot,
        color_continuous_scale="Inferno",
        aspect="auto",
        labels=dict(x="Namespace", y="Node", color="Risk"),
    )
    fig.update_layout(
        title="Node vs Namespace Risk Heatmap",
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="#fafafa"),
    )
    return fig


def _attack_chain_timeline(df: pd.DataFrame) -> go.Figure:
    chains = detect_chain(df.to_dict("records"))
    timeline_records = []
    for chain in chains:
        events = chain["events"]
        if not events:
            continue
        start = min(pd.to_datetime(e["timestamp"]) for e in events)
        end = max(pd.to_datetime(e["timestamp"]) for e in events)
        timeline_records.append(
            {
                "actor": chain["actor"],
                "source_ip": chain["source_ip"],
                "start": start,
                "finish": end,
                "score": chain["aggregate_score"],
            }
        )
    if not timeline_records:
        return go.Figure()
    timeline_df = pd.DataFrame(timeline_records)
    fig = px.timeline(
        timeline_df,
        x_start="start",
        x_end="finish",
        y="actor",
        color="score",
        hover_data=["source_ip"],
        color_continuous_scale="Plotly3",
    )
    fig.update_layout(
        title="Attack Chain Progression",
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="#fafafa"),
        yaxis_title="Actor",
    )
    fig.update_yaxes(autorange="reversed")
    return fig


def _alert_feed(df: pd.DataFrame) -> None:
    st.subheader("Active Alerts")
    top_alerts = df.sort_values(by="risk_score", ascending=False).head(10)
    for _, row in top_alerts.iterrows():
        risk = row["risk_score"]
        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            st.markdown(
                f"**{row['event']}** — `{row['pod']}` in `{row['cluster']}`\n"
                f"Severity: {row['severity']} | Risk: **{risk:.1f}** | Signals: {', '.join(row['signals'])}"
            )
        with col2:
            if st.button("Auto-Quarantine", key=f"quarantine-{row['id']}"):
                response = auto_quarantine(row["pod"])
                st.session_state.response_log.append(response)
        with col3:
            if st.button("Run Playbook", key=f"playbook-{row['id']}"):
                response = execute_playbook(row["id"])
                st.session_state.response_log.append(response)
        st.markdown("---")


def _compliance_cards(df: pd.DataFrame) -> None:
    st.subheader("Compliance Pulse")
    col1, col2, col3 = st.columns(3)
    compliance_targets = {
        "SOC2": 96 - df["risk_score"].mean() / 2,
        "HIPAA": 94 - df["severity"].mean(),
        "GDPR": 92 - df["risk_score"].std(),
    }
    for idx, (label, score) in enumerate(compliance_targets.items()):
        score = max(min(score, 100), 60)
        with (col1 if idx == 0 else col2 if idx == 1 else col3):
            st.metric(label=f"{label} posture", value=f"{score:.1f}%", delta="Stable" if score > 85 else "Needs review")


def _response_log_panel() -> None:
    st.subheader("Automated Response Journal")
    if not st.session_state.response_log:
        st.info("No automated responses triggered yet.")
        return
    st.json(st.session_state.response_log[-10:])


def _predictive_panel(df: pd.DataFrame) -> None:
    analyzer = RiskAnalyzer()
    events = df.to_dict("records")
    analyzer.fit(events)
    df["anomaly_score"] = analyzer.score_events(events)
    predictions = predict_next_stage(events)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(
            px.bar(
                df.groupby("cluster")["anomaly_score"].mean().reset_index(),
                x="cluster",
                y="anomaly_score",
                color="cluster",
                title="Cluster Anomaly Intensity",
                color_discrete_sequence=px.colors.sequential.Reds,
            ),
            use_container_width=True,
        )
    with col2:
        st.markdown("### Next Stage Predictions")
        for actor, stage in predictions.items():
            st.write(f"**{actor}** → *{stage}*")


def _threat_overview(df: pd.DataFrame) -> None:
    st.markdown(
        "<style>body {background-color: #0e1117;}</style>",
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Events", f"{len(df)}")
    c2.metric("Avg Severity", f"{df['severity'].mean():.1f}")
    c3.metric("Max Risk", f"{df['risk_score'].max():.1f}")
    c4.metric("Unique Pods", f"{df['pod'].nunique()}")


_ensure_state()

refresh_counter = st_autorefresh(interval=REFRESH_INTERVAL_MS, limit=None, key="secops-refresh")
if refresh_counter is not None:
    _refresh_events()

_df = _event_dataframe(st.session_state.events)

st.title("🛰️ AI-SecOps Command Center")

_threat_overview(_df)

col_map, col_heat = st.columns([3, 2])
with col_map:
    st.plotly_chart(_cluster_map(_df), use_container_width=True)
with col_heat:
    st.plotly_chart(_risk_heatmap(_df), use_container_width=True)

st.plotly_chart(_attack_chain_timeline(_df), use_container_width=True)

_alert_feed(_df)

_compliance_cards(_df)

st.markdown("### Predictive Analytics & Risk Forecast")
_predictive_panel(_df)

st.markdown("### Remediation Toolkit")
col_patch, col_quick = st.columns(2)
with col_patch:
    vuln = st.text_input("Key vulnerability", "CVE-2024-1337")
    if st.button("Generate Patch Recommendation"):
        st.session_state.response_log.append(generate_patch_recommendation(vuln))
with col_quick:
    pod = st.text_input("Target pod", "payments-0001")
    if st.button("Instant Quarantine"):
        st.session_state.response_log.append(auto_quarantine(pod))

_response_log_panel()
