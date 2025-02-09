import json
import time
import os
import subprocess
import requests
import zipfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def install_chrome_and_driver():
    """Manually installs Google Chrome & ChromeDriver in a non-root environment."""
    chrome_path = "/home/appuser/bin/google-chrome"
    chromedriver_path = "/home/appuser/bin/chromedriver"
    install_dir = "/home/appuser/bin"
    
    os.makedirs(install_dir, exist_ok=True)  # Ensure directory exists

    # 🟢 Install Google Chrome
    if not os.path.exists(chrome_path):
        print("🔹 Downloading Google Chrome...")
        chrome_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
        chrome_deb = os.path.join(install_dir, "google-chrome-stable_current_amd64.deb")

        response = requests.get(chrome_url, stream=True)
        with open(chrome_deb, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("🔹 Extracting Google Chrome...")
        subprocess.run(["dpkg-deb", "-x", chrome_deb, "chrome"], check=True)

        # 🟢 Use shutil.copytree() to copy the whole directory
        shutil.copytree("chrome/opt/google/chrome", chrome_path, dirs_exist_ok=True)

    # 🟢 Install ChromeDriver
    if not os.path.exists(chromedriver_path):
        print("🔹 Downloading ChromeDriver...")
        chromedriver_url = "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip"
        chromedriver_zip = os.path.join(install_dir, "chromedriver_linux64.zip")

        response = requests.get(chromedriver_url, stream=True)
        with open(chromedriver_zip, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("🔹 Extracting ChromeDriver...")
        with zipfile.ZipFile(chromedriver_zip, "r") as zip_ref:
            zip_ref.extractall(install_dir)

        shutil.copy(os.path.join(install_dir, "chromedriver"), chromedriver_path)  # Fix cross-device move
        os.chmod(chromedriver_path, 0o755)  # Make executable

# 🚀 Set up WebDriver
def get_webdriver():
    """Returns a properly configured WebDriver instance."""
    install_chrome_and_driver()  # Ensure Chrome & Driver are installed first

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 🟢 Explicitly set Chrome binary & Chromedriver path
    chrome_options.binary_location = "/home/appuser/bin/google-chrome"
    service = Service("/home/appuser/bin/chromedriver")

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ WebDriver initialized successfully!")
        return driver
    except Exception as e:
        print(f"❌ WebDriver failed to initialize: {e}")
        exit(1)

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
page_height = max(200, 120 * len(matches))

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

# ✅ Save the HTML file
html_file = "match_preview.html"
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

# ✅ Initialize WebDriver
driver = get_webdriver()

# 🌐 Load the generated HTML file in the browser
html_path = f"file://{os.path.abspath(html_file)}"
driver.get(html_path)
time.sleep(5)  # Allow rendering time

# 📏 Get total page height and resize window dynamically
total_height = driver.execute_script("return document.body.scrollHeight")
driver.set_window_size(800, total_height)

# 🖥️ Debugging Output
print("🖥️ Page Title:", driver.title)
print("📏 Page Height:", total_height)

# 📸 Capture Screenshot
screenshot_path = "match_preview.png"
try:
    driver.save_screenshot(screenshot_path)
    print(f"✅ Screenshot saved as {screenshot_path}")
except Exception as e:
    print(f"❌ Error capturing screenshot: {e}")

# 🚪 Close WebDriver
driver.quit()
