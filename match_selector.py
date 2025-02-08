import streamlit as st
import json

# Load match data
try:
    with open("matches.json", "r", encoding="utf-8") as file:
        matches = json.load(file)
except FileNotFoundError:
    matches = []

# Title
st.title("🎮 Select Matches")

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
