import requests, csv, json
from copy import deepcopy

def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Load config
with open("config.json") as f:
    config = json.load(f)

url = config["url"]
method = config.get("method", "GET").upper()
headers = config.get("headers", {})
base_payload = config.get("payload", {})

# Optional batch mode
batch = config.get("batch_mode", {})
is_batch = batch.get("enabled", False)

# Store all results here
all_flattened = []

if is_batch:
    field = batch["field"]
    csv_file = batch["csv_file"]

    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            zip_value = row[field]
            payload = deepcopy(base_payload)
            payload[field] = zip_value

            response = requests.request(method, url, headers=headers, json=payload)
            data = response.json()

            if isinstance(data, list):
                results = data
            elif isinstance(data, dict):
                list_candidates = [v for v in data.values() if isinstance(v, list)]
                results = list_candidates[0] if list_candidates else []
            else:
                results = []

            all_flattened.extend([flatten(r) for r in results])
else:
    response = requests.request(method, url, headers=headers, json=base_payload)
    data = response.json()
    if isinstance(data, list):
        all_flattened = [flatten(r) for r in data]
    elif isinstance(data, dict):
        list_candidates = [v for v in data.values() if isinstance(v, list)]
        rows = list_candidates[0] if list_candidates else []
        all_flattened = [flatten(r) for r in rows]

# Output CSV
if all_flattened:
    keys = sorted(set(k for row in all_flattened for k in row.keys()))
    with open("output.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in all_flattened:
            writer.writerow(row)
    print("✅ Done. Saved to output.csv")
else:
    print("⚠️ No data found.")
