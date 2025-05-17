import requests
import csv
import json

def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# 🔧 Load config from file
with open("config.json") as f:
    config = json.load(f)

url = config["url"]
method = config.get("method", "GET").upper()
headers = config.get("headers", {})
payload = config.get("payload", {})

# 📡 Make the API request
response = requests.request(method, url, headers=headers, json=payload)
data = response.json()

# 🧰 Find the list of records
if isinstance(data, list):
    rows = data
elif isinstance(data, dict):
    list_candidates = [v for v in data.values() if isinstance(v, list)]
    rows = list_candidates[0] if list_candidates else []
else:
    rows = []

# 🧹 Flatten nested fields
flat_rows = [flatten(row) for row in rows]

# 📁 Write to CSV
if flat_rows:
    keys = sorted(set(k for row in flat_rows for k in row.keys()))
    with open("output.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in flat_rows:
            writer.writerow(row)
    print("✅ Data saved to output.csv")
else:
    print("⚠️ No data found.")
