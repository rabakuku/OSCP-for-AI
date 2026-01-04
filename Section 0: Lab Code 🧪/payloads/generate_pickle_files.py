# generate_files.py

files_to_create = [
    "safe_model.pkl",        # Will trigger "Success"
    "infected_model.pkl",    # Will trigger "RCE Alert"
    "ransomware_model.pkl"   # Will trigger "Encryption Alert"
]

for filename in files_to_create:
    with open(filename, "w") as f:
        f.write("This is a dummy file for simulation testing.")
    print(f"✅ Created: {filename}")

print("\nFiles are ready! Upload them to the Streamlit app to test.")
