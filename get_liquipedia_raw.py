import requests
import json

# Liquipedia API endpoint
LIQUIPEDIA_API_URL = "https://liquipedia.net/counterstrike/api.php"

# API request parameters
PARAMS = {
    "action": "parse",
    "page": "Liquipedia:Matches",
    "format": "json",
    "prop": "text"
}

# Headers to prevent blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_liquipedia_raw():
    try:
        print("🌍 Fetching data from Liquipedia...")
        response = requests.get(LIQUIPEDIA_API_URL, headers=HEADERS, params=PARAMS, timeout=10)

        if response.status_code != 200:
            print(f"❌ Failed to fetch data. HTTP Status: {response.status_code}")
            return

        data = response.json()

        # Save raw data to liquipedia_raw.json
        with open("liquipedia_raw.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        print("✅ Raw data saved to liquipedia_raw.json!")

    except requests.exceptions.ConnectionError:
        print("❌ No internet connection. Please check your network.")

    except requests.exceptions.Timeout:
        print("❌ Request timed out. Liquipedia may be down.")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# Run the function
fetch_liquipedia_raw()
