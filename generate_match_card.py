import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# Load match data
with open("selected_matches.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

# Calculate dynamic page height (each match card ~100px + some padding)
page_height = max(200, 120 * len(matches))

# Generate HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Match Cards</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #333;
            color: white;
            text-align: center;
            padding: 20px;
            margin: 0;
            overflow: hidden; /* Removes scrollbar */
            height: {page_height}px; /* Dynamic height */
        }}
        .match-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
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
            width: auto;
            height: auto;
            object-fit: contain;
        }}
        .team {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .team-name {{
            font-size: 1.2em;
            font-weight: bold;
        }}
        .match-details {{
            flex: 1;
            text-align: center;
        }}
        .match-time {{
            font-size: 1.2em;
            color: #ddd;
        }}
        .match-score {{
            font-weight: bold;
            font-size: 1.4em;
        }}
    </style>
</head>
<body>
    <div class="match-container">
"""

for match in matches:
    html_content += f"""
    <div class="match-card">
        <div class="team">
            <img src="{match['logo1']}" alt="{match['team1']} logo">
            <span class="team-name">{match['team1']}</span>
        </div>
        <div class="match-details">
            <div class="match-time">{match['time'].split()[1]}</div>
            <div class="match-score">{match['score']}</div>
        </div>
        <div class="team">
            <span class="team-name">{match['team2']}</span>
            <img src="{match['logo2']}" alt="{match['team2']} logo">
        </div>
    </div>
    """

html_content += """
    </div>
</body>
</html>
"""

# Save HTML file
html_file = "match_preview.html"
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

# Open HTML preview
os.system(f"start {html_file}" if os.name == "nt" else f"xdg-open {html_file}")

# Setup Selenium WebDriver for rendering the HTML to an image
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Start Chrome with dynamic window size
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load HTML file in browser
html_path = f"file://{os.path.abspath(html_file)}"
driver.get(html_path)
time.sleep(2)  # Allow time for rendering

# Get total page height dynamically
total_height = driver.execute_script("return document.body.scrollHeight")
driver.set_window_size(800, total_height)  # Set dynamic height

# Take a screenshot
screenshot_path = "match_preview.png"
driver.save_screenshot(screenshot_path)
driver.quit()

# Save final image
print(f"Screenshot saved as {screenshot_path}")
