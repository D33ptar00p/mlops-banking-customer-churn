import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

def generate_sample_data(n_samples=1000, drift=False):
    data = []
    for _ in range(n_samples):
        # Features
        age = random.randint(18, 80)
        income = random.randint(20000, 150000)
        credit_score = random.randint(300, 850)
        
        # Logic for the 'Target' (Churn or Default)
        # If drift=True, we change the relationship to simulate a real-world shift
        noise = np.random.normal(0, 5000)
        if not drift:
            # High income/credit score usually means 0 (no default)
            target = 1 if (income < 40000 and credit_score < 500) else 0
        else:
            # Simulate a recession: even high credit scores are defaulting
            target = 1 if (income < 60000 or credit_score < 600) else 0
            
        data.append([age, income, credit_score, target])
    
    return pd.DataFrame(data, columns=['age', 'income', 'credit_score', 'target'])

# Save initial training set
df = generate_sample_data(2000)
df.to_csv("data/raw/train.csv", index=False)