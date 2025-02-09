import json
import os
from html2image import Html2Image

# ✅ Load match data safely
try:
    with open("selected_matches.json", "r", encoding="utf-8") as f:
        matches = json.load(f)
except FileNotFoundError:
    print("❌ `selected_matches.json` not found! Please ensure matches are selected before generating the card.")
    exit(1)

# ✅ Ensure logos exist for all matches
for match in matches:
    match['logo1'] = match.get('logo1', "https://via.placeholder.com/60")
    match['logo2'] = match.get('logo2', "https://via.placeholder.com/60")

# 📏 Calculate dynamic page height
page_height = max(400, 120 * len(matches))  # Ensure enough space for matches

# 📜 Generate HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Match Cards</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #333;
            color: white;
            text-align: center;
            padding: 20px;
            margin: 0;
            height: {page_height}px;
        }}
        .match-card {{
            background: #444;
            border-radius: 10px;
            padding: 15px;
            margin: 10px auto;
            width: 80%;
            max-width: 600px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }}
        .match-card img {{
            max-width: 60px;
            max-height: 60px;
        }}
    </style>
</head>
<body>
    <div class="match-container">
"""

for match in matches:
    html_content += f"""
    <div class="match-card">
        <div>
            <img src="{match['logo1']}" alt="{match['team1']} logo">
            <span>{match['team1']}</span>
        </div>
        <div>
            <div>{match['time'].split()[1]}</div>
            <div>{match.get('score', '? - ?')}</div>
        </div>
        <div>
            <span>{match['team2']}</span>
            <img src="{match['logo2']}" alt="{match['team2']} logo">
        </div>
    </div>
    """

html_content += """
    </div>
</body>
</html>
"""

# ✅ Generate Screenshot Without Chrome/Selenium
print("📸 Generating image using html2image...")

try:
    hti = Html2Image(output_path=".")
    hti.browser = 'firefox'  # Ensuring proper browser rendering
    hti.size = (800, page_height)  # Setting explicit size for the screenshot

    # Save the match preview image
    output_filename = "match_preview.png"
    hti.screenshot(html_str=html_content, save_as=output_filename)

    # ✅ Verify image generation
    if os.path.exists(output_filename):
        print(f"✅ Screenshot successfully saved: {output_filename}")
    else:
        print("❌ Error: Match card image not found after generation.")

except Exception as e:
    print(f"❌ Error generating screenshot: {e}")
