import sys
import os
import streamlit as st
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

st.title("📊 Top Player Statistics")

conn = get_connection()

st.subheader("🏏 Top 10 Run Scorers")

batting_query = """
SELECT 
    p.player_name,
    SUM(b.runs) AS total_runs,
    ROUND(AVG(b.runs), 2) AS avg_runs,
    MAX(b.runs) AS highest_score,
    ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
FROM batting_stats b
JOIN players p ON b.player_id = p.player_id
GROUP BY p.player_id, p.player_name
ORDER BY total_runs DESC
LIMIT 10;
"""

batting_df = pd.read_sql(batting_query, conn)
st.dataframe(batting_df, width="stretch")

st.subheader("🎯 Top 10 Wicket Takers")

bowling_query = """
SELECT 
    p.player_name,
    SUM(bs.wickets) AS total_wickets,
    ROUND(AVG(bs.economy), 2) AS avg_economy,
    SUM(bs.runs_given) AS total_runs_given
FROM bowling_stats bs
JOIN players p ON bs.player_id = p.player_id
GROUP BY p.player_id, p.player_name
ORDER BY total_wickets DESC
LIMIT 10;
"""

bowling_df = pd.read_sql(bowling_query, conn)
st.dataframe(bowling_df, width="stretch")

conn.close()