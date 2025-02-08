import streamlit as st
import json
import subprocess

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

    # Load match data
    try:
        with open("matches.json", "r", encoding="utf-8") as file:
            matches = json.load(file)
    except FileNotFoundError:
        matches = []

    # Search Bar
    search_query = st.text_input("🔍 Search for a match...")

    # Filter matches based on search query
    filtered_matches = [
        match for match in matches if search_query.lower() in f"{match['team1']} {match['team2']} {match['tournament']}".lower()
    ]

    # Store selections
    selected_matches = []

    # Display checkboxes for match selection
    for match in filtered_matches:
        match_text = f"{match['time']} - {match['team1']} vs {match['team2']} ({match['tournament']})"
        if st.checkbox(match_text):
            selected_matches.append(match)

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
        st.success("✅ Match Card Generated! Check `match_preview.png`")
