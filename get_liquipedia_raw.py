import requests
import json
import os
import subprocess

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

        # Save matches to `matches.json`
        with open("matches.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        print("✅ Matches saved to matches.json!")

        # Push the updated matches.json to GitHub
        push_to_github()

    except requests.exceptions.ConnectionError:
        print("❌ No internet connection. Please check your network.")

    except requests.exceptions.Timeout:
        print("❌ Request timed out. Liquipedia may be down.")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def push_to_github():
    """Automatically commit and push the updated `matches.json` file to GitHub."""
    try:
        repo_url = "https://github.com/YOUR_USERNAME/YOUR_REPO.git"  # Change this to your GitHub repo

        # Configure Git
        subprocess.run(["git", "config", "--global", "user.email", "you@example.com"])
        subprocess.run(["git", "config", "--global", "user.name", "Your Name"])

        # Add, commit, and push changes
        subprocess.run(["git", "add", "matches.json"])
        subprocess.run(["git", "commit", "-m", "Updated matches.json from Streamlit"])
        subprocess.run(["git", "push", repo_url, "main"])

        print("✅ matches.json pushed to GitHub!")

    except Exception as e:
        print(f"❌ Error pushing to GitHub: {e}")

# Run the function
fetch_liquipedia_raw()
