import streamlit as st
import json
import subprocess

st.set_page_config(page_title="Match Card Generator", layout="centered")

st.title("🎮 Match Card Generator")

# Buttons for each step
if st.button("1️⃣ Fetch Liquipedia Data"):
    subprocess.run(["python", "get_liquipedia_raw.py"])
    st.success("✅ Data Fetched Successfully!")

if st.button("2️⃣ Extract Matches"):
    subprocess.run(["python", "fetch_matches.py"])
    st.success("✅ Matches Extracted Successfully!")

if st.button("3️⃣ Select Matches"):
    subprocess.Popen(["python", "match_selector.py"])
    st.info("ℹ️ Match Selector Opened!")

if st.button("4️⃣ Generate Match Card"):
    subprocess.run(["python", "generate_match_card.py"])
    st.success("✅ Match Card Generated! Check `match_preview.png`")

# Show Selected Matches
st.subheader("📜 Selected Matches")
try:
    with open("selected_matches.json", "r") as file:
        selected_matches = json.load(file)
        st.write(selected_matches)
except FileNotFoundError:
    st.warning("⚠️ No matches selected yet.")

# Run the app locally
if __name__ == "__main__":
    st.write("💡 Click the buttons above to generate match cards!")
