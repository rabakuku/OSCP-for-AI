import streamlit as st
import os
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(page_title="Security Reports", layout="wide")

st.title("📊 LLM Vulnerability Reports")

# --- PATH LOGIC ---
# This finds the directory of the current script (pages/) and goes one level up to the root
current_dir = Path(__file__).parent
root_dir = current_dir.parent
# We look for reports in the 'pages' folder specifically now that you've moved them
report_dir = current_dir 

# List all HTML files in the pages directory
reports = [f for f in os.listdir(report_dir) if f.endswith('.html')]

if not reports:
    st.info(f"No reports found in {report_dir}. Move your .html files there or run a new scan!")
else:
    selected_report = st.selectbox("Choose a report to analyze:", sorted(reports, reverse=True))
    
    st.divider()
    
    # Construct the full path to the file
    file_path = report_dir / selected_report
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Display the report
    components.html(html_content, height=1000, scrolling=True)
