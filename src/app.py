from fastapi import FastAPI
import mlflow.pyfunc
import pandas as pd
import os
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import logging
from prometheus_client import Histogram, Counter

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MLOps Production API")

# Initializing prometheus monitoring to expore the /metrics endpoint
Instrumentator().instrument(app).expose(app)

# Defining histogram for specific features
# Buckets define the ranges we want to observe( e.g age ranges)
AGE_DISTRIBUTION = Histogram(
    'input_age_distribution',
    'Distribution of customer age in requests', 
    buckets=[18, 25, 35, 45, 55, 65, 100]
)

# Define a counter or historgram for predictions
PREDICTION_COUNT = Counter(
    'model_predtion_total',
    'Total count of churn vs no-churn predictions',
    ['outcome']
)

# Configuration
MODEL_NAME = "customer-churn-model"
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Global variable to hold the model
model = None

class PredictionInput(BaseModel):
    # Bank client data
    age: int
    job: str
    marital: str
    education: str
    default: str
    housing: str
    loan: str
    
    # Related with the last contact of the current campaign
    contact: str
    month: str
    day_of_week: str
    duration: int
    
    # Other attributes
    campaign: int
    pdays: int
    previous: int
    poutcome: str
    
    # Social and economic context attributes (updated names)
    emp_var_rate: float
    cons_price_idx: float
    cons_conf_idx: float
    euribor3m: float
    nr_employed: float

@app.on_event("startup")
def load_model():
    global model
    # Fetching by "production" alias ensures we get the vetted version
    model_uri = f"models:/{MODEL_NAME}@production"
    model = mlflow.pyfunc.load_model(model_uri)
    print(f"✅ Loaded model: {MODEL_NAME} from {model_uri}")

@app.get("/health")
def health():
    return {"status": "ready", "model": MODEL_NAME}

@app.post("/predict")
def predict(data: PredictionInput):

    # Record observations for monitoring
    AGE_DISTRIBUTION.observe(data.age)

    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)

    # Track teh prediction result
    PREDICTION_COUNT.labels(outcome=str(int(prediction))).inc()

    return {"prediction": int(prediction[0])}