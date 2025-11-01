"""Streamlit application for the AI SecOps platform demo."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import streamlit as st
import yaml

from agents.security_agents import IncidentCommanderAgent, build_agent_registry
from analytics.behavior import detect_anomalies, fingerprint_user
from analytics.explainability import generate_sample_features, lime_explanation, shap_summary
from analytics.federated import FederatedNode, simulate_federated_round, synthetic_dataset
from analytics.rl_optimizer import FirewallOptimizer
from compliance.blockchain import AuditLedger
from compliance.scanner import run_continuous_scan
from compliance.soar import trigger_playbook
from core.chaos_injector import inject_failure
from core.crypto import certificate_metadata
from core.gitops import progressive_deploy, record_change
from core.kafka_pipeline import KafkaPipeline, bootstrap_pipeline, simulate_threat_event
from core.quantum_entropy import entropy_strength, harvest_entropy
from core.secops_stream_processor import derive_threat_summary, process_stream
from core.self_healing import evaluate_exploit_detection, predictive_patching
from core.vector_store import VectorStore
from core.xdr_connectors import CONNECTOR_SOURCES, fetch_events, unified_schema
from core.zero_trust import ZeroTrustGateway

st.set_page_config(page_title="AI SecOps Demo", layout="wide")

# ---------------------------------------------------------------------------
# Session bootstrap
# ---------------------------------------------------------------------------
if "registry" not in st.session_state:
    st.session_state.registry = build_agent_registry()
    st.session_state.commander = st.session_state.registry.get("IncidentCommanderAgent")

if "pipeline" not in st.session_state:
    pipeline = KafkaPipeline()
    bootstrap_pipeline(pipeline, sample_size=15)
    st.session_state.pipeline = pipeline

if "vector_store" not in st.session_state:
    store = VectorStore()
    store.add("ransomware", "Ransomware T1486 encryption patterns", {"ttp": "T1486"})
    store.add("lateral", "Lateral movement credential abuse", {"ttp": "T1021"})
    st.session_state.vector_store = store

if "ledger" not in st.session_state:
    st.session_state.ledger = AuditLedger()

if "optimizer" not in st.session_state:
    st.session_state.optimizer = FirewallOptimizer()

if "zt_gateway" not in st.session_state:
    gateway = ZeroTrustGateway(trust_domain="ai-secops.local")
    st.session_state.zt_gateway = gateway
    for workload in ("streamlit", "fastapi", "flink", "agents"):
        identity = gateway.register_workload(workload)
        st.session_state.ledger.append({"event": f"workload_registered:{identity.spiffe_id}"})

# ---------------------------------------------------------------------------
# Load tenant configuration
# ---------------------------------------------------------------------------
config_path = Path("configs/tenants.yaml")
TENANT_CONFIG = yaml.safe_load(config_path.read_text()) if config_path.exists() else {}

st.sidebar.title("Enterprise Controls")
tenant = st.sidebar.selectbox("Select environment", options=list(TENANT_CONFIG.keys())) if TENANT_CONFIG else "prod"
new_change = st.sidebar.text_input("GitOps change summary")
if st.sidebar.button("Record Change") and new_change:
    change = record_change(environment=tenant, author="demo", summary=new_change)
    st.session_state.ledger.append({"event": f"gitops:{change.summary}"})
    st.sidebar.success(f"Change queued for {tenant}")

# ---------------------------------------------------------------------------
# Streaming pipeline simulation
# ---------------------------------------------------------------------------
for _ in range(3):
    st.session_state.pipeline.publish("threat-events", simulate_threat_event())

messages = st.session_state.pipeline.drain()
enriched = process_stream(messages)
summary = derive_threat_summary(enriched)

st.title("Future-Ready AI SecOps Platform")

col1, col2, col3, col4 = st.columns(4)
col1.metric("High Severity", summary.get("high", 0))
col2.metric("Medium Severity", summary.get("medium", 0))
col3.metric("Low Severity", summary.get("low", 0))
col4.metric("Average Risk", summary.get("average_risk", 0.0))

if enriched:
    enriched_df = pd.DataFrame(enriched)
    st.subheader("Unified Threat Timeline")
    st.dataframe(enriched_df)

# ---------------------------------------------------------------------------
# Ask SecOps NLP interface
# ---------------------------------------------------------------------------
st.subheader("Ask SecOps - Autonomous Orchestration")
question = st.text_input("Pose a question or incident description", "Investigate anomalous Okta logins")
if st.button("Run Playbook"):
    incident = {"description": question, "priority": "high", "indicators": ["okta", "login"], "anomaly_score": 0.92}
    commander: IncidentCommanderAgent = st.session_state.commander
    plan = commander.coordinate(incident)
    st.json(plan)
    st.session_state.ledger.append({"event": f"plan:{plan['recommendation']}"})

# ---------------------------------------------------------------------------
# Vector intelligence search
# ---------------------------------------------------------------------------
st.subheader("Threat Intelligence Search")
query = st.text_input("Search TTPs", "lateral movement")
results = st.session_state.vector_store.search(query)
st.write(results)

# ---------------------------------------------------------------------------
# Zero-trust view
# ---------------------------------------------------------------------------
st.subheader("Zero-Trust Gateway")
caller = st.selectbox("Caller", options=list(st.session_state.zt_gateway._policies.keys()))
callee = st.selectbox("Callee", options=list(st.session_state.zt_gateway._policies.keys()))
allowed = st.session_state.zt_gateway.authorize(caller, callee)
payload = f"{caller}->{callee}"
signature = st.session_state.zt_gateway.sign_request(caller, payload)
metadata = certificate_metadata(st.session_state.zt_gateway._policies[caller][1])
st.write({"authorized": allowed, "signature_valid": st.session_state.zt_gateway.verify_signature(caller, payload, signature), "metadata": metadata})

# ---------------------------------------------------------------------------
# Quantum entropy visualisation
# ---------------------------------------------------------------------------
st.subheader("Quantum Entropy Source")
entropy_pool = harvest_entropy(64)
st.write({"entropy_strength": entropy_strength(entropy_pool), "sample": entropy_pool[:10]})

# ---------------------------------------------------------------------------
# Federated analytics and RL optimisation
# ---------------------------------------------------------------------------
st.subheader("Federated Threat Analytics")
dataset = synthetic_dataset()
chunk = len(dataset) // 3
nodes: List[FederatedNode] = []
for i in range(3):
    start = i * chunk
    end = (i + 1) * chunk if i < 2 else len(dataset)
    nodes.append(FederatedNode(name=f"node-{i}", data=dataset[start:end], differential_privacy_epsilon=1.0 + i))
round_result = simulate_federated_round(nodes)
st.write(round_result)

st.subheader("Adaptive Firewall Optimizer")
telemetry = list(np.random.default_rng().uniform(0, 1, 20))
optimizer_result = st.session_state.optimizer.simulate_episode(telemetry)
st.write({"q_table": st.session_state.optimizer.q_table, "latest": optimizer_result})

# ---------------------------------------------------------------------------
# Behavior analytics
# ---------------------------------------------------------------------------
st.subheader("Behavior Analytics")
users = {f"user{i}": fingerprint_user(f"user{i}", {"device": f"dev{i}", "location": "global"}) for i in range(3)}
st.write(detect_anomalies(list(users.values())))

# ---------------------------------------------------------------------------
# Compliance automation
# ---------------------------------------------------------------------------
st.subheader("Compliance Automation")
scan = run_continuous_scan(tenant, assets=["prod-cluster", "edge-gateway"])
st.write(scan)
st.subheader("SOAR Playbook")
st.write(trigger_playbook("containment", {"tenant": tenant}))

st.subheader("Immutable Audit Trail")
st.table(pd.DataFrame(st.session_state.ledger.as_dict()))

# ---------------------------------------------------------------------------
# XDR integrations
# ---------------------------------------------------------------------------
st.subheader("Extended Detection & Response")
connector_cols = st.columns(len(CONNECTOR_SOURCES))
for idx, (key, label) in enumerate(CONNECTOR_SOURCES.items()):
    events = [unified_schema(event) for event in fetch_events(key)]
    connector_cols[idx].write({"connector": label, "events": events})

# ---------------------------------------------------------------------------
# Explainable AI dashboard
# ---------------------------------------------------------------------------
st.subheader("Explainable AI")
features = generate_sample_features(50)


def _model_predict(data: np.ndarray) -> np.ndarray:
    """Lightweight surrogate model used for XAI examples."""

    return 0.4 * data[:, 0] + 0.3 * data[:, 1] + 0.2 * data[:, 2] + 0.1 * data[:, 3]

shap_result = shap_summary(_model_predict, features)
lime_result = lime_explanation(_model_predict, features)
st.write({"shap": shap_result, "lime": lime_result})

# ---------------------------------------------------------------------------
# Self-healing triggers
# ---------------------------------------------------------------------------
st.subheader("Self-Healing Automation")
if enriched:
    top_risk = max(event.get("risk_score", 0.0) for event in enriched)
else:
    top_risk = 0.0
st.write(evaluate_exploit_detection(top_risk))
st.write(predictive_patching(vuln_score=0.87))

# ---------------------------------------------------------------------------
# Chaos testing and resilience
# ---------------------------------------------------------------------------
st.subheader("Chaos Engineering")
st.write(inject_failure())

st.subheader("Progressive Deployment")
st.write(progressive_deploy(TENANT_CONFIG.get(tenant, {}).get("regions", [tenant])))

st.caption("Detection accuracy 99.9%+ simulated | Automated containment <10s | Transparent XAI insights")
