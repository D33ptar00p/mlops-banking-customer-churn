import pandas as pd
import requests
import zipfile
import io
import os

def ingest_data():
    # This is the main container URL
    url = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"
    raw_path = "data/raw"
    os.makedirs(raw_path, exist_ok=True)
    
    print(f"Downloading main container from {url}...")
    response = requests.get(url)
    
    # 1. Open the main container
    with zipfile.ZipFile(io.BytesIO(response.content)) as outer_zip:
        # 2. Open the 'bank-additional.zip' located inside the main zip
        with outer_zip.open('bank-additional.zip') as nested_zip_file:
            # 3. Read the content of the nested zip into memory
            nested_data = io.BytesIO(nested_zip_file.read())
            
            with zipfile.ZipFile(nested_data) as inner_zip:
                # 4. Finally, open the actual CSV
                # 'bank-additional-full.csv' is the most complete version (41k+ rows)
                target_file = 'bank-additional/bank-additional-full.csv'
                with inner_zip.open(target_file) as f:
                    # NOTE: This dataset uses ';' as a separator!
                    df = pd.read_csv(f, sep=';')
                    
                    # Save a clean version for our pipeline
                    output_file = f"{raw_path}/train.csv"
                    df.to_csv(output_file, index=False)
                    
                    print(f"✅ Success! Ingested {len(df)} rows into {output_file}")

if __name__ == "__main__":
    ingest_data()