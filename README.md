# 🧹 JSON to CSV Extractor

A simple Python tool that takes an API returning JSON and saves it as a CSV.  
Perfect for quickly turning public API data into spreadsheets — no scraping required.

---

## 🚀 How It Works

You provide:
- An API endpoint
- Request type (`GET` or `POST`)
- Optional headers and payload (for filtering, auth, etc.)

The script:
1. Sends the API request
2. Parses the JSON
3. Flattens nested fields like `address.zipcode`
4. Writes everything to `output.csv`

---

## 📄 Example `config.json`

```json
{
  "url": "https://jsonplaceholder.typicode.com/users",
  "method": "GET",
  "headers": {},
  "payload": {}
}
```
## For a POST request
```json
{
  "url": "https://example.com/api/search",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN"
  },
  "payload": {
    "zipcode": "90210",
    "last_name": "Smith"
  }
}
```

## Usage
1. Clone the repo or download the files
2. Edit config.json with the API info
3. Run the script:
```python extractor.py```
4. Your flattened csv should appear as output.csv

## Requirements
```pip install requests```