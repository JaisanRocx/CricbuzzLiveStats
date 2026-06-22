import sys
import os
import streamlit as st
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

st.title("🏠 Home Dashboard")

conn = get_connection()

def get_count(table):
    df = pd.read_sql(f"SELECT COUNT(*) AS total FROM {table}", conn)
    return int(df["total"][0])

col1, col2, col3 = st.columns(3)
col1.metric("Matches", get_count("matches"))
col2.metric("Players", get_count("players"))
col3.metric("Series", get_count("series"))

col4, col5, col6 = st.columns(3)
col4.metric("Venues", get_count("venues"))
col5.metric("Batting Records", get_count("batting_stats"))
col6.metric("Bowling Records", get_count("bowling_stats"))

st.subheader("📌 Project Overview")
st.write("""
This project integrates Cricbuzz API data with a MySQL database and Streamlit dashboard.

Features:
- Real-time cricket match insights
- Player batting and bowling statistics
- SQL-based analytics
- CRUD operations for player management
""")

conn.close()