import streamlit as st
import json
import subprocess
import os
import sys

# 🚀 Set Streamlit page configuration
st.set_page_config(page_title="Match Card Generator", layout="wide")

# ✅ Function to Ensure Required Packages Are Installed
def ensure_package_installed(package_name):
    """Ensures a package is installed in the correct environment."""
    try:
        __import__(package_name)
    except ModuleNotFoundError:
        print(f"⚠️ {package_name} module not found! Installing now...")

        # 🛠 Use --user to avoid permission errors
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", package_name])

        # ✅ Add site-packages path for proper module recognition
        package_path = os.path.expanduser("~/.local/lib/python3.10/site-packages")
        if package_path not in sys.path:
            sys.path.append(package_path)

        # 🚨 Retry importing the package after installation
        try:
            __import__(package_name)
        except ModuleNotFoundError:
            print(f"❌ Failed to install {package_name}. Check permissions or dependencies.")

# 🚨 Ensure Required Packages Exist
ensure_package_installed("requests")
ensure_package_installed("beautifulsoup4")
ensure_package_installed("lxml")

# ✅ Debugging Information
print(f"🔍 sys.path: {sys.path}")
print(f"🔍 Python Executable: {sys.executable}")
print(f"🔍 Installed Packages:")
subprocess.run([sys.executable, "-m", "pip", "list"])

# 🎮 Sidebar Navigation
page = st.sidebar.radio("🔍 Navigate", ["🏠 Home", "🎯 Select Matches", "📸 Generate Match Card"])

# 🏠 Home Page
if page == "🏠 Home":
    st.title("🎮 Match Card Generator")

    if st.button("1️⃣ Fetch Liquipedia Data"):
        result = subprocess.run(["python", "get_liquipedia_raw.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("✅ Data Fetched Successfully!")
        else:
            st.error(f"❌ Error fetching data:\n{result.stderr}")

    if st.button("2️⃣ Extract Matches"):
        result = subprocess.run(["python", "fetch_matches.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("✅ Matches Extracted Successfully!")
        else:
            st.error(f"❌ Error extracting matches:\n{result.stderr}")

# 🎯 Select Matches Page
elif page == "🎯 Select Matches":
    st.title("🎯 Select Matches")

    # Load match data with error handling
    try:
        with open("matches.json", "r", encoding="utf-8") as file:
            matches = json.load(file)
        if not matches:
            st.warning("⚠️ No matches found. Please fetch matches first!")
    except FileNotFoundError:
        st.error("❌ `matches.json` not found! Run `fetch_matches.py` first.")
        matches = []

    # 🔍 Search Bar
    search_query = st.text_input("🔍 Search for a match...")

    # 🔎 Filter matches based on search query
    filtered_matches = [
        match for match in matches if search_query.lower() in f"{match['team1']} {match['team2']} {match['tournament']}".lower()
    ]

    # ✅ Store selected matches
    selected_matches = []

    # 📌 Display checkboxes for match selection
    if filtered_matches:
        for i, match in enumerate(filtered_matches):
            match_text = f"{match['time']} - {match['team1']} vs {match['team2']} ({match['tournament']})"
            if st.checkbox(match_text, key=f"match_{i}"):  # Ensure unique key
                selected_matches.append(match)
    else:
        st.warning("⚠️ No matches available. Try fetching data first!")

    # 💾 Save selected matches
    if st.button("✅ Save Selected Matches"):
        with open("selected_matches.json", "w", encoding="utf-8") as file:
            json.dump(selected_matches, file, indent=2)
        st.success("✅ Selected matches saved successfully!")

# 📸 Generate Match Card Page
elif page == "📸 Generate Match Card":
    st.title("📸 Generate Match Card")

    if st.button("🎨 Generate Match Card"):
        result = subprocess.run(["python", "generate_match_card.py"], capture_output=True, text=True)
        if result.returncode == 0:
            image_path = os.path.abspath("match_preview.png")  # Ensure absolute path
            if os.path.exists(image_path):
                st.success("✅ Match Card Generated! Download below.")
                with open(image_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Match Card",
                        data=file,
                        file_name="match_preview.png",
                        mime="image/png"
                    )
            else:
                st.error("❌ Match card image not found. Try regenerating.")
        else:
            st.error(f"❌ Error generating match card:\n{result.stderr}")
