import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")

st.write("""
Welcome to the Cricbuzz LiveStats dashboard.

Use the sidebar to navigate:
- Home Dashboard
- Live Matches
- Top Player Stats
- SQL Analytics
- CRUD Operations
""")