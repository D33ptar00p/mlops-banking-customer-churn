import os
import pandas as pd
import mlflow
import yaml
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def train():
    # Load hyperparameters from params.yaml
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)["train"]

    df = pd.read_csv("data/processed/train.csv")
    
    # 1. Separate Features and Target
    X = df.drop("y", axis=1)
    # Convert target 'yes'/'no' to 1/0
    #y = df["y"].apply(lambda x: 1 if x == "yes" else 0)
    y = df["y"]

    # 2. Identify Column Types
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()
    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # 3. Create Preprocessing Layers
    # We use OneHotEncoder for categories and StandardScaler for numbers
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
        ]
    )

    # 4. Create the Full Pipeline
    # This bundle (Preprocess + Model) is what we will save to MLflow
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=params["n_estimators"], max_depth=params["max_depth"]))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=params["seed"])

    # MLflow Setup
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.set_experiment("Customer_Churn_Experiment")
    with mlflow.start_run():
        # Autolog will now capture the ENTIRE pipeline
        mlflow.sklearn.autolog()
        
        model_pipeline.fit(X_train, y_train)
        
        y_pred = model_pipeline.predict(X_test)
        print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    train()