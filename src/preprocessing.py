"""Preprocessing and feature engineering utilities."""
import logging
import pandas as pd
import os

logger = logging.getLogger(__name__)

def preprocess():
    input_path = "data/raw/train.csv"
    output_path = "data/processed/train.csv"
    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_csv(input_path)

    # 1. Fix column names (replace '.' with '_') 
    # This is crucial because Python doesn't like dots in variables
    df.columns = [c.replace(".", "_") for c in df.columns]

    # 2. Encode Target (convert 'yes'/'no' to 1/0)
    df['y'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)

    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to {output_path}")

if __name__ == "__main__":
    preprocess()
