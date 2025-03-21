import pandas as pd
import requests
import time

# Load CSV File
file_path = "./data/lopucki_data_cusip.csv"  # Replace with actual file path
df = pd.read_csv(file_path)

# Combine cusip6 and cusip9 to create full CUSIP
df["CUSIP"] = df["Cusip6"].astype(str) + df["Cusip9"].astype(str)

# OpenFIGI API details
OPENFIGI_API_URL = "https://api.openfigi.com/v3/mapping"
HEADERS = {"Content-Type": "application/json"}

def get_tickers_from_cusips(cusips, retries=3):
    """
    Fetches ticker symbols from OpenFIGI for a batch of CUSIPs.
    Retries failed requests up to 'retries' times.
    """
    payload = [{"idType": "ID_CUSIP", "idValue": cusip} for cusip in cusips]
    
    for attempt in range(retries):
        try:
            response = requests.post(OPENFIGI_API_URL, json=payload, headers=HEADERS)
            
            # If no response or error, retry
            if response.status_code != 200 or not response.text.strip():
                print(f"Retrying API request... (Attempt {attempt+1}/{retries})")
                time.sleep(1)  # Wait before retrying
                continue
            
            data = response.json()
            
            tickers = []
            for item in data:
                if "data" in item and item["data"]:
                    tickers.append(item["data"][0]["ticker"])
                else:
                    tickers.append(None)  # No ticker found
            
            return tickers  # If successful, return results

        except Exception as e:
            print(f"Error fetching tickers: {e}")
            time.sleep(1)  # Wait before retrying
    
    return [None] * len(cusips)  # If all retries fail, return None

# Process in batches of 5 to reduce API calls
batch_size = 5
tickers = []

for i in range(0, len(df), batch_size):
    batch_cusips = df["CUSIP"].iloc[i:i+batch_size].tolist()
    batch_tickers = get_tickers_from_cusips(batch_cusips)
    tickers.extend(batch_tickers)
    
    print(f"Processed {min(i+batch_size, len(df))}/{len(df)} companies...")
    time.sleep(0.5)  # Prevent API rate limits

# Add tickers to DataFrame
df["Ticker"] = tickers

# Save results to a new CSV file
output_file = "companies_with_tickers.csv"
df.to_csv(output_file, index=False)

print(f"✅ Data saved to {output_file}. Open it to view results.")