# 🚀 End-to-End MLOps: Banking Churn Prediction System

This project implements a production-grade MLOps lifecycle to predict customer churn using the UCI Bank Marketing dataset. It demonstrates how to bridge the gap between a notebook-based experiment and a stable, monitored, and containerized microservice.



## 🏗️ System Architecture
This project follows the **MLOps Level 1 maturity model**, ensuring that every model in production can be traced back to its specific code, data, and hyperparameters.

* **Data Versioning:** [DVC](https://dvc.org/) (Data Version Control) with local/remote storage.
* **Experiment Tracking:** [MLflow](https://mlflow.org/) used for logging metrics, parameters, and model signatures.
* **Model Serving:** [FastAPI](https://fastapi.tiangolo.com/) microservice wrapped in Docker.
* **Infrastructure:** Multi-container orchestration using **Docker Compose** (PostgreSQL, MLflow Server, and API).

---

## 📂 Project Structure
```text
├── data/               # Versioned by DVC (ignored by Git)
│   ├── raw/            
|       ├── train.csv   # Raw UCI Bank Marketing dataset
│   └── processed/      
|       ├── train.csv   # Cleaned and preprocessed data
├── src/
│   ├── ingestion.py     # Downloads and extracts nested UCI data
│   ├── preprocessing.py # Cleans features and targets
│   ├── train.py         # Pipeline training with MLflow autologging
│   └── app.py           # FastAPI prediction service
├── docker-compose.yml   # Orchestrates the full stack
├── Dockerfile           # Production build for the API
├── dvc.yaml             # DVC pipeline definition
└── params.yaml          # Centralized hyperparameters
