from fastapi import FastAPI
import mlflow.pyfunc
import pandas as pd
import os
from pydantic import BaseModel

app = FastAPI(title="MLOps Production API")

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
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)
    return {"prediction": int(prediction[0])}