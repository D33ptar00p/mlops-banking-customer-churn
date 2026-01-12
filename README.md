# 🚀 End-to-End MLOps: Banking Churn Prediction System

This project implements a production-grade MLOps lifecycle to predict customer churn using the UCI Bank Marketing dataset. It demonstrates how to bridge the gap between a notebook-based experiment and a stable, monitored, and containerized microservice.



## 🏗️ System Architecture
This project follows the **MLOps Level 1 maturity model**, ensuring that every model in production can be traced back to its specific code, data, and hyperparameters.

* **Data & Pipeline Versioning:** [DVC](https://dvc.org/) orchestrates the entire ML pipeline (ingestion, preprocessing, training) and versions the data and models, ensuring full reproducibility.
* **Experiment Tracking:** [MLflow](https://mlflow.org/) used for logging metrics, parameters, and model signatures.
* **Model Serving:** [FastAPI](https://fastapi.tiangolo.com/) microservice wrapped in Docker.
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
│   ├── preprocessing.py # Cleans features and targets
│   ├── train.py         # Pipeline training with MLflow autologging
│   └── app.py           # FastAPI prediction service
├── docker-compose.yml   # Orchestrates the full stack
├── Dockerfile           # Defines the production build for the API
├── dvc.yaml             # Defines the DVC pipeline stages (ingest, preprocess, train)
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
