# AI-SecOps Kubernetes Security Monitoring Demo

This project showcases an investor-ready, AI-assisted Kubernetes security operations center. It combines synthetic eBPF-style telemetry, lightweight ML analytics, and a futuristic Streamlit dashboard.

## Features

- **Agent Simulator** – Generates syscall, file-integrity, crypto-mining, and audit anomalies per cluster.
- **Threat Correlation** – Scores events, reconstructs attack chains, and predicts kill-chain progression.
- **ML Analytics** – IsolationForest-based anomaly scoring with cluster summaries.
- **Live Dashboard** – Real-time threat map, heatmap, attack timeline, alerts, compliance pulse, and remediation toolkit.
- **Response Automation** – Simulated quarantine, playbook execution, and patch recommendations.

## Getting Started

```bash
cd k8s-sec-monitor
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The dashboard auto-refreshes every five seconds and continuously injects new synthetic threats.

## Project Structure

```
/k8s-sec-monitor/
├── app.py
├── agents/
│   ├── __init__.py
│   └── simulator.py
├── core/
│   ├── __init__.py
│   ├── correlation.py
│   └── response.py
├── ml/
│   ├── __init__.py
│   └── analyzer.py
├── data/
│   └── sample_events.json
├── requirements.txt
└── README.md
```

## Demo Tips

- Use the **Auto-Quarantine** or **Run Playbook** buttons in the alert feed to populate the response journal.
- Adjust the vulnerability or pod fields in the *Remediation Toolkit* to simulate SecOps workflows.
- Highlight predictive insights by focusing on the *Next Stage Predictions* panel.

## Extending the Demo

- Integrate real telemetry by replacing `agents/simulator.py` with real collectors.
- Swap the heuristic scorer in `core/correlation.py` for a production-grade risk model.
- Connect `core/response.py` to orchestration tooling (e.g., Argo Workflows, Ansible) for live actions.

Enjoy exploring the AI-powered SecOps future! 🚀
