import requests
import json

# Liquipedia API endpoint for Counter-Strike matches
LIQUIPEDIA_API_URL = "https://liquipedia.net/counterstrike/api.php"

# API parameters to fetch Liquipedia:Matches page in raw JSON format
PARAMS = {
    "action": "parse",
    "page": "Liquipedia:Matches",
    "format": "json",
    "prop": "text"
}

# Headers to mimic a browser request (prevents blocking)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_liquipedia_raw():
    response = requests.get(LIQUIPEDIA_API_URL, headers=HEADERS, params=PARAMS)

    if response.status_code != 200:
        print("❌ Failed to fetch Liquipedia API data.")
        return None

    data = response.json()

    # Save raw JSON to file
    with open("liquipedia_raw.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    print("✅ Successfully saved Liquipedia raw data to 'liquipedia_raw.json'!")

# Run the function
fetch_liquipedia_raw()
