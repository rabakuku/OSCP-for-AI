# generate_audio_files.py

files_to_create = [
    "secure_meeting.mp3",      # Will trigger "Success" (Safe)
    "injection_attempt.wav",   # Will trigger "Security Block" (Keyword detected)
    "subtle_command.mp3"       # Will trigger "XML Tagging" (Defense in Depth)
]

for filename in files_to_create:
    # We create empty files. The Streamlit app only checks the name.
    with open(filename, "wb") as f:
        f.write(b"Dummy audio content") 
    print(f"✅ Created: {filename}")

print("\nFiles are ready! Upload them to the Streamlit app to test.")
