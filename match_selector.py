import json
import customtkinter as ctk

# Configure the CustomTkinter Theme
ctk.set_appearance_mode("dark")  # "light", "dark", or "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

# Load match data
with open("matches.json", "r", encoding="utf-8") as file:
    matches = json.load(file)

# Create a list of match selections
selected_matches = []
match_vars = {}  # Dictionary to store checkboxes and their variables

def toggle_match(match, var):
    """Toggle selection of a match"""
    if var.get() and match not in selected_matches:
        selected_matches.append(match)
    elif not var.get() and match in selected_matches:
        selected_matches.remove(match)

def generate_display():
    """Save selected matches and close the window"""
    with open("selected_matches.json", "w", encoding="utf-8") as file:
        json.dump(selected_matches, file, indent=2)
    print("✅ Selected matches saved!")
    root.destroy()  # Close the window after saving

def update_match_list(search_text=""):
    """Update the match list based on search input"""
    for widget in frame.winfo_children():
        widget.destroy()  # Clear the frame before adding filtered matches

    for match in matches:
        match_text = f"{match['time']} - {match['team1']} vs {match['team2']} ({match['tournament']})"
        
        # Show only matches that contain the search text
        if search_text.lower() in match_text.lower():
            var = ctk.BooleanVar()
            match_vars[match_text] = var
            btn = ctk.CTkCheckBox(frame, text=match_text, variable=var, command=lambda m=match, v=var: toggle_match(m, v))
            btn.pack(anchor="w", padx=10, pady=2)

# Create the main window
root = ctk.CTk()
root.title("Match Selector")
root.geometry("600x550")

# Title Label
title_label = ctk.CTkLabel(root, text="🎮 Select Matches", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Search Bar
search_var = ctk.StringVar()
search_entry = ctk.CTkEntry(root, textvariable=search_var, placeholder_text="🔍 Search matches...", width=500)
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", lambda e: update_match_list(search_var.get()))  # Update list on typing

# Scrollable Frame for Match List
frame = ctk.CTkScrollableFrame(root, width=580, height=350)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Initially populate the match list
update_match_list()

# Generate Button
generate_btn = ctk.CTkButton(root, text="✅ Save & Close", command=generate_display, height=40, width=250)
generate_btn.pack(pady=10)

# Run the GUI
root.mainloop()
