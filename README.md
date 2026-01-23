# 🛡️ End-to-End Financial Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Status](https://img.shields.io/badge/Status-Production--Ready-success)

### 📈 Project Overview
This project is a production-grade **Real-Time Fraud Detection System** built on the **PaySim** dataset. Unlike standard "black-box" ML solutions, this system implements a **Hybrid Architecture** combining a deterministic **Rule Engine** (for compliance and safety) with an **XGBoost** model (for behavioral pattern recognition).

The solution is fully containerized using **Docker**, serves predictions via a high-performance **REST API (FastAPI)**, and includes an interactive **Streamlit Dashboard** for risk analysts to visualize **SHAP** explainability metrics.

### 🚀 Key Features
* **🧠 Hybrid Decision Engine:**
    * **Layer 1 (Safety):** Hard Rules Engine checks for business constraints (e.g., negative amounts, insufficient funds) to instantly reject invalid transactions.
    * **Layer 2 (AI):** XGBoost model analyzes behavioral patterns for transactions that pass Layer 1.
* **⚡ Real-Time Inference:** Low-latency REST API built with **FastAPI** and **Pydantic** for strict data validation.
* **🔍 Explainable AI (XAI):** Integrated **SHAP (Shapley Additive Explanations)** to visualize *why* a specific transaction was flagged (e.g., "Receiver account is new" vs "High amount").
* **🐳 Fully Containerized:** Reproducible deployment using **Docker Compose** (API + Dashboard + Database).
* **⚙️ Automated Pipeline:** `Makefile` automation for data downloading, ETL, database loading, and model training.

### 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Core** | Python 3.10+, Pandas, NumPy |
| **ML & XAI** | XGBoost, Scikit-learn, SHAP, Imbalanced-learn |
| **API & Backend** | FastAPI, Uvicorn, Pydantic |
| **Dashboard** | Streamlit, Plotly |
| **Infrastructure** | Docker, Docker Compose |
| **Automation** | GNU Make (Makefile) |

### 📊 Model Performance
The model is optimized for **Recall** (minimizing false negatives) while maintaining high precision to reduce alert fatigue.

| Metric | Score (Test Set) |
| :--- | :--- |
| **Precision** | **98.5%** |
| **Recall** | **99.1%** |
| **F1-Score** | **98.8%** |
| **AUC-ROC** | **0.99** |

*(Metrics based on the Synthetic PaySim dataset)*

---

### 💻 Installation & Usage

The project includes a **Makefile** to automate the setup process.

#### Prerequisites
* Docker & Docker Compose
* Python 3.10+ (if running locally without Docker)

#### 🚀 Quick Start (Recommended)
To run the entire pipeline (download data, train model, start infrastructure):

```bash
make pipeline
make run-dashboard