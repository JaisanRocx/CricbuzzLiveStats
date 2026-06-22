import streamlit as st
import pandas as pd
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

st.title("🏏 Live Scoreboard")
st.caption("Live / recent cricket scoreboard using Cricbuzz API data stored in MySQL")

conn = get_connection()

scoreboard_query = """
SELECT
    m.match_id,
    m.series_name,
    m.match_desc,
    m.match_format,
    m.team1,
    m.team2,
    m.venue,
    m.city,
    m.status,
    COALESCE(b.total_runs, 0) AS total_runs,
    COALESCE(b.total_fours, 0) AS total_fours,
    COALESCE(b.total_sixes, 0) AS total_sixes,
    COALESCE(b.highest_score, 0) AS highest_score,
    COALESCE(w.total_wickets, 0) AS total_wickets
FROM matches m
LEFT JOIN (
    SELECT
        match_id,
        SUM(runs) AS total_runs,
        SUM(fours) AS total_fours,
        SUM(sixes) AS total_sixes,
        MAX(runs) AS highest_score
    FROM batting_stats
    GROUP BY match_id
) b ON m.match_id = b.match_id
LEFT JOIN (
    SELECT
        match_id,
        SUM(wickets) AS total_wickets
    FROM bowling_stats
    GROUP BY match_id
) w ON m.match_id = w.match_id
ORDER BY m.start_date DESC
LIMIT 30;
"""

df = pd.read_sql(scoreboard_query, conn)

if df.empty:
    st.warning("No scoreboard data found.")
else:
    st.subheader("📋 Match Scoreboard")

    st.dataframe(df, width="stretch")

    df["match_label"] = (
        df["team1"] + " vs " + df["team2"] + " - " + df["match_desc"]
    )

    selected_match = st.selectbox(
        "Select a match to view full scorecard",
        df["match_label"]
    )

    selected_row = df[df["match_label"] == selected_match].iloc[0]
    match_id = int(selected_row["match_id"])

    st.subheader("🏆 Match Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Runs", int(selected_row["total_runs"]))
    col2.metric("Total Wickets", int(selected_row["total_wickets"]))
    col3.metric("Total Fours", int(selected_row["total_fours"]))
    col4.metric("Total Sixes", int(selected_row["total_sixes"]))

    st.write("### Match Details")

    st.write(f"**Series:** {selected_row['series_name']}")
    st.write(f"**Teams:** {selected_row['team1']} vs {selected_row['team2']}")
    st.write(f"**Format:** {selected_row['match_format']}")
    st.write(f"**Venue:** {selected_row['venue']}, {selected_row['city']}")
    st.write(f"**Status:** {selected_row['status']}")

    st.divider()

    st.subheader("🏏 Batting Scorecard")

    batting_query = """
    SELECT
        COALESCE(NULLIF(p.player_name, ''), CONCAT('Player ', b.player_id)) AS player_name,
        b.runs,
        b.balls,
        b.fours,
        b.sixes,
        b.strike_rate
    FROM batting_stats b
    LEFT JOIN players p ON b.player_id = p.player_id
    WHERE b.match_id = %s
    ORDER BY b.runs DESC;
    """

    batting_df = pd.read_sql(batting_query, conn, params=(match_id,))
    st.dataframe(batting_df, width="stretch")

    if not batting_df.empty:
        st.bar_chart(batting_df.set_index("player_name")["runs"])

    st.subheader("🎯 Bowling Scorecard")

    bowling_query = """
    SELECT
        COALESCE(NULLIF(p.player_name, ''), CONCAT('Player ', bw.player_id)) AS player_name,
        bw.overs,
        bw.maidens,
        bw.wickets,
        bw.runs_given,
        bw.economy
    FROM bowling_stats bw
    LEFT JOIN players p ON bw.player_id = p.player_id
    WHERE bw.match_id = %s
    ORDER BY bw.wickets DESC;
    """

    bowling_df = pd.read_sql(bowling_query, conn, params=(match_id,))
    st.dataframe(bowling_df, width="stretch")

    if not bowling_df.empty:
        st.bar_chart(bowling_df.set_index("player_name")["wickets"])

conn.close()