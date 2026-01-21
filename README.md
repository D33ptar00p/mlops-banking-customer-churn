# 🚀 End-to-End MLOps: Banking Churn Prediction System

This project implements a production-grade MLOps lifecycle to predict customer churn using the UCI Bank Marketing dataset. It demonstrates how to bridge the gap between a notebook-based experiment and a stable, monitored, and containerized microservice.



## 🏗️ System Architecture
This project follows the **MLOps Level 1 maturity model**, ensuring that every model in production can be traced back to its specific code, data, and hyperparameters.

* **Data & Pipeline Versioning:** [DVC](https://dvc.org/) orchestrates the entire ML pipeline (ingestion, preprocessing, training) and versions the data and models, ensuring full reproducibility.
* **Experiment Tracking:** [MLflow](https://mlflow.org/) used for logging metrics, parameters, and model signatures.
* **Model Serving:** [FastAPI](https://fastapi.tiangolo.com/) microservice wrapped in Docker.
* **Monitoring & Observability:** **Prometheus** for metrics collection (e.g., API latency, request rates) and **Grafana** for visualization and dashboarding.
* **Infrastructure:** Multi-container orchestration using **Docker Compose** (PostgreSQL DB, MLflow Server, and API).

---

## 📂 Project Structure
```text
├── data/               # Versioned by DVC (ignored by Git)
│   ├── raw/            
│       └── train.csv   # Raw UCI Bank Marketing dataset
│   └── processed/      
│       └── train.csv   # Cleaned and preprocessed data
├── src/
│   ├── ingestion.py     # Downloads and extracts nested UCI data
│   ├── preprocessing.py # Cleans features and prepares data
│   ├── train.py         # Pipeline training with MLflow autologging
│   └── app.py           # FastAPI prediction service
├── monitoring/
│   └── prometheus.yml   # Prometheus scrape configurations
├── docker-compose.yml   # Orchestrates the full stack
├── Dockerfile           # Defines the production build for the API
├── dvc.yaml             # Defines the DVC pipeline stages (ingest, preprocess, train)
├── requirements.txt     # Python dependencies
└── params.yaml          # Centralized hyperparameters
```

## 🛠️ Setup & Running Instructions

## Prerequisites
Ensure you have the following installed:
*   Python 3.10+
*   Docker & Docker Compose
*   Git
*   DVC (install with `pip install dvc`)

## Environment Initialization
Clone the repository and set up your virtual environment to run the pipeline scripts.


### Clone the repository
```bash
git clone [https://github.com/D33ptar00p/mlops-banking-customer-churn.git](https://github.com/D33ptar00p/mlops-banking-customer-churn.git)
cd mlops-banking-churn
```

### Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Launch Infrastructure
Start the backend services (PostgreSQL, MLflow Tracking Server, and the Prediction API) using Docker Compose.

```Bash

docker-compose up -d --build
```

## Access Points:

🟢 MLflow Tracking UI: http://localhost:5000

🔵 API Documentation: http://localhost:8000/docs

🟡 Grafana Dashboards: http://localhost:3000 (Default login: `admin`/`admin`)

⚫ Prometheus Targets: http://localhost:9090

## Execute the Full ML Pipeline (DVC)
Use a single DVC command to run the entire pipeline: data ingestion, preprocessing, and model training. DVC automatically checks dependencies and runs only the necessary stages.

```Bash

# This command will execute the 'ingest', 'preprocess', and 'train' stages
# defined in dvc.yaml in the correct order.
dvc repro
```

The pipeline performs the following actions:
1.  **`ingest`**: Runs `src/ingestion.py` to download the dataset.
2.  **`preprocess`**: Runs `src/preprocessing.py` to clean the data.
3.  **`train`**: Runs `src/train.py` to train the model, log experiments to MLflow, and save the final model artifact (`models/model.pkl`) for DVC to track.

5. Register the Model in MLflow

After the pipeline completes, promote the best model to be used by the API.


1. Open the MLflow UI at http://localhost:5000.
Click on the most recent run in the "Customer_Churn_Experiment".

Scroll to Artifacts and click Register Model.

Name the model customer-churn-model.

Under the Models tab, select version 1 and set the Alias to Production.

6. Load the New Model in the API
The API is configured to fetch the model aliased as `@Production` on startup. Restart the API service to make it load your newly registered model.

```Bash
docker-compose restart api
```

7. Test the Prediction Endpoint
Use cURL to verify the end-to-end flow:

```Bash
curl -X 'POST' 'http://localhost:8000/predict' \
-H 'Content-Type: application/json' \
-d '{
  "age": 35, "job": "management", "marital": "married", "education": "university.degree",
  "default": "no", "housing": "yes", "loan": "no", "contact": "cellular",
  "month": "aug", "day_of_week": "fri", "duration": 200, "campaign": 1,
  "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp_var_rate": 1.4,
  "cons_price_idx": 93.444, "cons_conf_idx": -36.1, "euribor3m": 4.963, "nr_employed": 5228.1
}'
```

# 📈 Observability & ML Monitoring

This project implements a comprehensive observability stack using **Prometheus** and **Grafana** to monitor both the **REST API (Operational Health)** and the **Machine Learning Model (Data & Prediction Health)**.

---

## 🏗️ Monitoring Architecture



1.  **FastAPI (The Exporter):** Uses `prometheus-fastapi-instrumentator` to expose a `/metrics` endpoint.
2.  **Prometheus (The Collector):** Periodically "scrapes" the API for metrics and stores them in a time-series database.
3.  **Grafana (The Visualizer):** Connects to Prometheus to display real-time dashboards and trigger alerts.

---

## 🔍 What are we monitoring?

### 1. API Operational Health (The "Golden Signals")
We track the stability and performance of the prediction service:
* **Request Volume (RPS):** Total requests per second hitting the `/predict` endpoint.
* **Latency (P95/P99):** Time taken to process a prediction. Crucial for detecting if the model becomes too slow under load.
* **Error Rates:** Monitoring `4xx` (bad data) and `5xx` (server crash) status codes.

### 2. ML Model Monitoring
This section is unique to MLOps and focuses on detecting **Data Drift** and **Model Performance**:
* **Prediction Distribution:** A bar chart/pie chart showing the ratio of `0` (No Churn) vs `1` (Churn) predictions. 
    > *Insight: If the model suddenly predicts 100% "Churn", we may have Model Drift.*
* **Feature Distribution (Age/Duration):** Histograms of incoming feature values.
    > *Insight: If the average customer age in production is 60, but the model was trained on age 25, we have Data Drift.*
* **Model Loading Status:** Tracks if the API is successfully pulling the `@production` model from the MLflow registry.

---

## 🛠️ Accessing the Dashboards

Once your Docker containers are running (`docker-compose up -d`), you can access the monitoring suite at:

| Service | URL | Purpose |
| :--- | :--- | :--- |
| **Prometheus** | `http://localhost:9090` | Query raw metrics using PromQL |
| **Grafana** | `http://localhost:3000` | View real-time visual dashboards |
| **API Metrics** | `http://localhost:8000/metrics` | Raw data being exposed by the API |

**Default Grafana Credentials:** `admin` / `admin`

The default datasource added to Grafana is Promethues through the `datasource.yml` file.
Two dashboards are added:
* **FastAPI Observability:** For observing performance of the API
* **ML Dashboard:** For MLOps Observability like prediction distribution, input distribution which could help with drift detection

---
## 🧪 Running the Smoke Test
A smoke test script (`tests/smoke_test.py`) is provided to simulate traffic to the API and generate metrics for visualization.

To run the smoke test, execute:

```bash
python tests/smoke_test.py
```

To generate data continuosly:

```bash
while true; do python tests/smoke_test.py; sleep 60; done
```
---

