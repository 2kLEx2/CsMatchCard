import streamlit as st
import json
import subprocess
import os
import sys

# Ensure requests is installed
try:
    import requests
except ModuleNotFoundError:
    print("⚠️ requests module not found! Installing now...")
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"])
    import requests  # Try importing again after install

import streamlit as st

st.set_page_config(page_title="Match Card Generator", layout="wide")

# Sidebar Navigation
page = st.sidebar.radio("🔍 Navigate", ["🏠 Home", "🎯 Select Matches", "📸 Generate Match Card"])

# Home Page
if page == "🏠 Home":
    st.title("🎮 Match Card Generator")

    if st.button("1️⃣ Fetch Liquipedia Data"):
        subprocess.run(["python", "get_liquipedia_raw.py"])
        st.success("✅ Data Fetched Successfully!")

    if st.button("2️⃣ Extract Matches"):
        subprocess.run(["python", "fetch_matches.py"])
        st.success("✅ Matches Extracted Successfully!")

# Select Matches Page
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

    # Search Bar
    search_query = st.text_input("🔍 Search for a match...")

    # Filter matches based on search query
    filtered_matches = [
        match for match in matches if search_query.lower() in f"{match['team1']} {match['team2']} {match['tournament']}".lower()
    ]

    # Store selections
    selected_matches = []

    # Display checkboxes for match selection with unique keys
    if filtered_matches:
        for i, match in enumerate(filtered_matches):
            match_text = f"{match['time']} - {match['team1']} vs {match['team2']} ({match['tournament']})"
            if st.checkbox(match_text, key=f"match_{i}"):  # Ensure unique key
                selected_matches.append(match)

    else:
        st.warning("⚠️ No matches available. Try fetching data first!")

    # Save selected matches
    if st.button("✅ Save Selected Matches"):
        with open("selected_matches.json", "w", encoding="utf-8") as file:
            json.dump(selected_matches, file, indent=2)
        st.success("✅ Selected matches saved successfully!")

# Generate Match Card Page
elif page == "📸 Generate Match Card":
    st.title("📸 Generate Match Card")

    if st.button("🎨 Generate Match Card"):
        subprocess.run(["python", "generate_match_card.py"])
        
        image_path = os.path.abspath("match_preview.png")  # Ensure absolute path
        if os.path.exists(image_path):
            st.success("✅ Match Card Generated! Download below.")
            with open(image_path, "rb") as file:
                btn = st.download_button(
                    label="📥 Download Match Card",
                    data=file,
                    file_name="match_preview.png",
                    mime="image/png"
                )
        else:
            st.error("❌ Match card image not found. Try regenerating.")
