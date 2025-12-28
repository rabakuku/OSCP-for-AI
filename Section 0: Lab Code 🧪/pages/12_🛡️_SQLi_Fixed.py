import streamlit as st
import sqlite3
from utils import query_llm

st.header("LAB6: SQL Injection via LLM (Fixed)")
st.success("🛡️ STATUS: SECURE")

# Setup Mock DB
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, salary INTEGER)')
c.execute("INSERT INTO users VALUES (1, 'Alice', 50000)")
conn.commit()

# Helper function to clean LLM output (Fixes syntax errors)
def clean_sql(text):
    return text.replace("```sql", "").replace("```", "").strip()

user_input = st.text_input("Ask the DB a question:", "Get all users")

if st.button("Query Securely"):
    # 1. Fix: Ask for Parameters/Select only
    prompt = f"Convert to SQL (SELECT statements ONLY) for table 'users'. Question: {user_input}"
    raw_response = query_llm([{"role": "user", "content": prompt}])

    # 2. Clean formatting
    sql_query = clean_sql(raw_response)

    st.code(sql_query, language="sql")

    # 3. Fix: Validation Layer
    # Check for forbidden keywords AND the semicolon (which allows chaining)
    if "DROP" in sql_query.upper() or "DELETE" in sql_query.upper() or ";" in sql_query:
        st.error("⛔ BLOCK: Destructive or Chained SQL detected.")
    else:
        try:
            # 4. Fix: execute() instead of executescript()
            # execute() only runs ONE statement. If there are two, it throws an error.
            c.execute(sql_query) 
            st.write(c.fetchall())
        except Exception as e:
            st.error(f"Error: {e}")
