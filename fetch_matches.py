import json
import datetime
from bs4 import BeautifulSoup

# Load raw Liquipedia data
with open("liquipedia_raw.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract HTML content
html_content = data["parse"]["text"]["*"]

# Parse HTML using BeautifulSoup (MUCH FASTER than regex)
soup = BeautifulSoup(html_content, "lxml")

formatted_matches = []

# Find all match tables (Correct class: "infobox_matches_content")
match_tables = soup.find_all("table", class_="infobox_matches_content")

for table in match_tables:
    rows = table.find_all("tr")

    # Extract team names, scores, event, and match time
    try:
        team1 = rows[0].find("td", class_="team-left").text.strip()
        team2 = rows[0].find("td", class_="team-right").text.strip()
        score = rows[0].find("td", class_="versus").text.strip()

        # Extract timestamp from second row
        timestamp = int(rows[1].find("span", class_="timer-object").get("data-timestamp"))
        match_time = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')

        # Extract team logos
        logo1 = "https://liquipedia.net" + rows[0].find("td", class_="team-left").find("img")["src"]
        logo2 = "https://liquipedia.net" + rows[0].find("td", class_="team-right").find("img")["src"]

        # Extract tournament name
        tournament = rows[1].find("a").text.strip()

        formatted_matches.append({
            "team1": team1,
            "team2": team2,
            "score": score,
            "tournament": tournament,
            "time": match_time,
            "logo1": logo1,
            "logo2": logo2
        })

    except Exception as e:
        print(f"⚠️ Skipping match due to error: {e}")

# Save extracted matches to JSON
with open("matches.json", "w", encoding="utf-8") as file:
    json.dump(formatted_matches, file, indent=2)

print(f"✅ Extracted {len(formatted_matches)} matches successfully!")
