import requests
import random
import time

# API Endpoint
URL = "http://localhost:8000/predict"

# Feature Options (matching UCI Bank dataset categories)
JOBS = ["management", "blue-collar", "technician", "admin.", "services", "retired"]
MARITAL = ["married", "single", "divorced"]
EDUCATION = ["university.degree", "high.school", "basic.9y", "professional.course"]
MONTHS = ["may", "jun", "jul", "aug", "oct", "nov"]
DAYS = ["mon", "tue", "wed", "thu", "fri"]
POUTCOMES = ["nonexistent", "failure", "success"]

def generate_random_data():
    """Generates a random banking customer profile"""
    # We bias 'duration' occasionally to trigger a '1' (Churn) for monitoring
    duration = random.randint(50, 3000) if random.random() > 0.8 else random.randint(10, 500)
    
    return {
        "age": random.randint(18, 80),
        "job": random.choice(JOBS),
        "marital": random.choice(MARITAL),
        "education": random.choice(EDUCATION),
        "default": "no",
        "housing": random.choice(["yes", "no"]),
        "loan": random.choice(["yes", "no"]),
        "contact": random.choice(["cellular", "telephone"]),
        "month": random.choice(MONTHS),
        "day_of_week": random.choice(DAYS),
        "duration": duration,
        "campaign": random.randint(1, 5),
        "pdays": 999 if random.random() > 0.1 else random.randint(1, 20),
        "previous": random.randint(0, 2),
        "poutcome": random.choice(POUTCOMES),
        "emp_var_rate": round(random.uniform(-3.4, 1.4), 1),
        "cons_price_idx": round(random.uniform(92.2, 94.8), 3),
        "cons_conf_idx": round(random.uniform(-50.8, -26.9), 1),
        "euribor3m": round(random.uniform(0.6, 5.0), 3),
        "nr_employed": round(random.uniform(4963.0, 5228.0), 1)
    }

def run_smoke_test(num_requests=100):
    print(f"🚀 Starting smoke test: Sending {num_requests} requests...")
    success_count = 0
    
    for i in range(num_requests):
        data = generate_random_data()
        try:
            response = requests.post(URL, json=data)
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"❌ Request {i} failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"⚠️ Connection error on request {i}: {e}")
        
        # Small sleep to simulate realistic traffic flow
        time.sleep(0.1)
        
        if (i + 1) % 10 == 0:
            print(f"✅ Sent {i + 1}/{num_requests} requests...")

    print(f"\n✨ Smoke test complete! Successfully processed {success_count} predictions.")
    print("👉 Check your Grafana dashboard at http://localhost:3000 to see the results.")

if __name__ == "__main__":
    run_smoke_test()