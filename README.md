# ArsenicGuard

# ArsenicGuard: An Explainable AI Agent for Groundwater Arsenic Risk Assessment and Decision Support in Bangladesh

ArsenicGuard is a distributed, production-grade Explainable AI (XAI) and Adaptive Decision Support system engineered to predict groundwater arsenic contamination risks in Bangladesh. Built upon the comprehensive DPHE/BGS National Hydrochemical Survey dataset (2,386 spatial aquifer records), this system bridges high-precision machine learning with transparent, human-interpretable linguistic insights and structural recommendations.

Target Conference: **ICCIT 2026 (IEEE)**

---

## 🔥 Key Technical Highlights (Novelty Area)

*   **Distributed Architecture:** Decoupled framework deploying a high-performance **FastAPI backend API** (`server.py`) and an interactive **Streamlit frontend portal** (`app.py`).
*   **Predictive Core (XGBoost):** Optimized ensemble engine delivering a generalized testing accuracy of **82.64%**, F1-Score of **75.80%**, and a highly robust **ROC-AUC of 0.9017**.
*   **Adaptive AI Agent Framework:** The agent dynamically pivots its operational strategies into 3 distinct behavioral tiers (`LOW`, `MEDIUM`, and `HIGH` Risk Strategies) aligned directly with global **WHO** and domestic **DPHE Bangladesh** safe water thresholds.
*   **Counterfactual Reasoning Optimization:** An built-in mathematical engine loops through features to compute exactly how much hydro-chemical metrics (e.g., Iron level) must be mitigated to structurally flip an unsafe prediction into a safe zone.
*   **Human Review Trigger:** Evaluates prediction uncertainties statefully. The agent flags borderline probability boundaries (40% ≤ P ≤ 60%) and dynamically prompts a standard laboratory re-verification protocol.
*   **Post-Hoc Explainability (XAI):** Decodes computational black-boxes using **SHAP (SHapley Additive exPlanations)** to establish global and local feature dependencies (Depth, Iron, Manganese, Spatial Coordinates).

---

## 📁 Repository Structure

*   `server.py`: Asynchronous production-ready FastAPI backend exposing strict schema-validated inference endpoints.
*   `app.py`: Dual-language (Bangla/English) cognitive user dashboard executing feature sliders for real-time What-If optimization.
*   `arsenic_guard_model.json`: Pre-compiled, regularized optimal XGBoost classifier serialized for zero-latency runtime caching.
*   `requirements.txt`: Python package configuration dependencies matching Python 3.14 system baselines.

---

## ⚡ Quick Start: One-Click Pipeline Execution

To initiate the fully distributed environment locally via Jupyter Notebook or terminal, invoke the following sub-processing macro:

```python
import subprocess
import time

# 1. Boot up FastAPI Production Core (Port 8000)
backend_process = subprocess.Popen(["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"])
time.sleep(3) 

# 2. Deploy Headless Streamlit Frontend Portal (Port 8501)
frontend_process = subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"])
```

Access client analytics on `http://localhost:8501` and interactive API docs on `http://localhost:8000/docs`.
