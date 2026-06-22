import sys
import os
import streamlit as st
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

st.title("🔍 SQL Analytics")

conn = get_connection()

queries = {
    "1. Indian Players": """
        SELECT player_name, role, batting_style, bowling_style
        FROM players
        WHERE country = 'Ireland';
    """,

    "2. Recent Matches": """
        SELECT match_desc, team1, team2, venue, city, status
        FROM matches
        ORDER BY start_date DESC
        LIMIT 20;
    """,

    "3. Top 10 ODI Run Scorers": """
        SELECT 
            p.player_name,
            SUM(b.runs) AS total_runs,
            ROUND(AVG(b.runs), 2) AS batting_average,
            SUM(CASE WHEN b.runs >= 100 THEN 1 ELSE 0 END) AS centuries
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        WHERE m.match_format = 'ODI'
        GROUP BY p.player_id, p.player_name
        ORDER BY total_runs DESC
        LIMIT 10;
    """,

    "4. Venues Capacity Above 25000": """
        SELECT venue_name, city, country, capacity
        FROM venues
        WHERE capacity > 25000
        ORDER BY capacity DESC
        LIMIT 10;
    """,

    "5. Matches Played by Each Team": """
        SELECT team_name, COUNT(*) AS total_matches
        FROM (
            SELECT team1 AS team_name FROM matches
            UNION ALL
            SELECT team2 AS team_name FROM matches
        ) AS t
        GROUP BY team_name
        ORDER BY total_matches DESC;
    """,

    "6. Players by Role": """
        SELECT role, COUNT(*) AS total_players
        FROM players
        GROUP BY role
        ORDER BY total_players DESC;
    """,

    "7. Highest Score by Format": """
        SELECT 
            m.match_format,
            MAX(b.runs) AS highest_score
        FROM batting_stats b
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY m.match_format
        ORDER BY highest_score DESC;
    """,

    "8. Series in 2024": """
        SELECT 
            series_name,
            match_format,
            COUNT(*) AS total_matches
        FROM matches
        WHERE YEAR(FROM_UNIXTIME(start_date / 1000)) = 2024
        GROUP BY series_name, match_format
        ORDER BY series_name;
    """,

    "9. All Rounder Performance": """
        SELECT 
            p.player_name,
            SUM(b.runs) AS total_runs,
            SUM(bs.wickets) AS total_wickets
        FROM players p
        JOIN batting_stats b ON p.player_id = b.player_id
        JOIN bowling_stats bs ON p.player_id = bs.player_id
        GROUP BY p.player_id, p.player_name
        HAVING total_runs > 100 AND total_wickets > 5
        ORDER BY total_runs DESC;
    """,

    "10. Last 20 Completed Matches": """
        SELECT match_desc, team1, team2, status, venue, city
        FROM matches
        WHERE status IS NOT NULL
        ORDER BY start_date DESC
        LIMIT 20;
    """,

    "11. Player Runs by Format": """
        SELECT 
            p.player_name,
            SUM(CASE WHEN m.match_format = 'TEST' THEN b.runs ELSE 0 END) AS test_runs,
            SUM(CASE WHEN m.match_format = 'ODI' THEN b.runs ELSE 0 END) AS odi_runs,
            SUM(CASE WHEN m.match_format IN ('T20', 'T20I') THEN b.runs ELSE 0 END) AS t20_runs,
            ROUND(AVG(b.runs), 2) AS overall_average
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY p.player_id, p.player_name
        ORDER BY overall_average DESC;
    """,

    "12. Team Performance by Venue": """
        SELECT team_name, venue, city, COUNT(*) AS matches_played
        FROM (
            SELECT team1 AS team_name, venue, city FROM matches
            UNION ALL
            SELECT team2 AS team_name, venue, city FROM matches
        ) AS t
        GROUP BY team_name, venue, city
        ORDER BY matches_played DESC
        LIMIT 20;
    """,

    "13. Batting Partnerships": """
        SELECT 
            p1.player_name AS player_1,
            p2.player_name AS player_2,
            b1.match_id,
            (b1.runs + b2.runs) AS combined_runs
        FROM batting_stats b1
        JOIN batting_stats b2 
            ON b1.match_id = b2.match_id
           AND b1.player_id < b2.player_id
        JOIN players p1 ON b1.player_id = p1.player_id
        JOIN players p2 ON b2.player_id = p2.player_id
        WHERE (b1.runs + b2.runs) >= 100
        ORDER BY combined_runs DESC
        LIMIT 20;
    """,

    "14. Bowling Performance by Venue": """
        SELECT 
            p.player_name,
            m.venue,
            COUNT(DISTINCT bs.match_id) AS matches_played,
            SUM(bs.wickets) AS total_wickets,
            ROUND(AVG(bs.economy), 2) AS avg_economy
        FROM bowling_stats bs
        JOIN players p ON bs.player_id = p.player_id
        JOIN matches m ON bs.match_id = m.match_id
        GROUP BY p.player_id, p.player_name, m.venue
        ORDER BY total_wickets DESC
        LIMIT 20;
    """,

    "15. Player Performance in Matches": """
        SELECT 
            p.player_name,
            COUNT(*) AS matches_played,
            SUM(b.runs) AS total_runs,
            ROUND(AVG(b.runs), 2) AS avg_runs
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY avg_runs DESC
        LIMIT 20;
    """,

    "16. Batting Performance by Year": """
        SELECT 
            p.player_name,
            YEAR(FROM_UNIXTIME(m.start_date / 1000)) AS match_year,
            COUNT(*) AS matches_played,
            ROUND(AVG(b.runs), 2) AS avg_runs,
            ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY p.player_id, p.player_name, match_year
        ORDER BY match_year DESC, avg_runs DESC;
    """,

    "17. Toss Advantage": """
        SELECT 
            'Toss data is not available in current database' AS answer;
    """,

    "18. Most Economical Bowlers": """
        SELECT 
            p.player_name,
            COUNT(DISTINCT bs.match_id) AS matches_played,
            SUM(bs.wickets) AS total_wickets,
            ROUND(AVG(bs.economy), 2) AS economy_rate
        FROM bowling_stats bs
        JOIN players p ON bs.player_id = p.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY economy_rate ASC
        LIMIT 10;
    """,

    "19. Most Consistent Batsmen": """
        SELECT 
            p.player_name,
            COUNT(*) AS innings_played,
            ROUND(AVG(b.runs), 2) AS avg_runs,
            ROUND(STDDEV(b.runs), 2) AS consistency_score
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.balls >= 10
        GROUP BY p.player_id, p.player_name
        ORDER BY consistency_score ASC
        LIMIT 10;
    """,

    "20. Matches and Average by Format": """
        SELECT 
            p.player_name,
            COUNT(CASE WHEN m.match_format = 'TEST' THEN 1 END) AS test_matches,
            ROUND(AVG(CASE WHEN m.match_format = 'TEST' THEN b.runs END), 2) AS test_avg,
            COUNT(CASE WHEN m.match_format = 'ODI' THEN 1 END) AS odi_matches,
            ROUND(AVG(CASE WHEN m.match_format = 'ODI' THEN b.runs END), 2) AS odi_avg,
            COUNT(CASE WHEN m.match_format IN ('T20', 'T20I') THEN 1 END) AS t20_matches,
            ROUND(AVG(CASE WHEN m.match_format IN ('T20', 'T20I') THEN b.runs END), 2) AS t20_avg
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY p.player_id, p.player_name
        ORDER BY p.player_name;
    """,

    "21. Player Performance Ranking": """
        SELECT 
            p.player_name,
            COALESCE(SUM(b.runs), 0) AS total_runs,
            COALESCE(ROUND(AVG(b.runs), 2), 0) AS batting_average,
            COALESCE(ROUND(AVG(b.strike_rate), 2), 0) AS strike_rate,
            COALESCE(SUM(bs.wickets), 0) AS total_wickets,
            COALESCE(ROUND(AVG(bs.economy), 2), 0) AS economy_rate,
            ROUND(
                COALESCE(SUM(b.runs), 0) * 0.01 +
                COALESCE(AVG(b.runs), 0) * 0.5 +
                COALESCE(AVG(b.strike_rate), 0) * 0.3 +
                COALESCE(SUM(bs.wickets), 0) * 2,
                2
            ) AS performance_score
        FROM players p
        LEFT JOIN batting_stats b ON p.player_id = b.player_id
        LEFT JOIN bowling_stats bs ON p.player_id = bs.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY performance_score DESC
        LIMIT 20;
    """,

    "22. Head to Head Teams": """
        SELECT 
            LEAST(team1, team2) AS team_a,
            GREATEST(team1, team2) AS team_b,
            COUNT(*) AS total_matches
        FROM matches
        GROUP BY LEAST(team1, team2), GREATEST(team1, team2)
        ORDER BY total_matches DESC
        LIMIT 20;
    """,

    "23. Recent Player Form": """
        SELECT 
            p.player_name,
            COUNT(*) AS innings_played,
            ROUND(AVG(b.runs), 2) AS avg_runs,
            ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate,
            SUM(CASE WHEN b.runs >= 50 THEN 1 ELSE 0 END) AS scores_above_50,
            CASE
                WHEN AVG(b.runs) >= 50 THEN 'Excellent Form'
                WHEN AVG(b.runs) >= 30 THEN 'Good Form'
                WHEN AVG(b.runs) >= 15 THEN 'Average Form'
                ELSE 'Poor Form'
            END AS form_status
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY avg_runs DESC
        LIMIT 20;
    """,

    "24. Successful Batting Pairs": """
        SELECT 
            p1.player_name AS player_1,
            p2.player_name AS player_2,
            COUNT(*) AS partnerships,
            ROUND(AVG(b1.runs + b2.runs), 2) AS avg_combined_runs,
            SUM(CASE WHEN (b1.runs + b2.runs) >= 50 THEN 1 ELSE 0 END) AS fifty_plus_partnerships,
            MAX(b1.runs + b2.runs) AS highest_combined_score
        FROM batting_stats b1
        JOIN batting_stats b2 
            ON b1.match_id = b2.match_id
           AND b1.player_id < b2.player_id
        JOIN players p1 ON b1.player_id = p1.player_id
        JOIN players p2 ON b2.player_id = p2.player_id
        GROUP BY b1.player_id, b2.player_id, p1.player_name, p2.player_name
        ORDER BY avg_combined_runs DESC
        LIMIT 20;
    """,

    "25. Quarterly Player Trend": """
        SELECT 
            p.player_name,
            CONCAT(
                YEAR(FROM_UNIXTIME(m.start_date / 1000)),
                '-Q',
                QUARTER(FROM_UNIXTIME(m.start_date / 1000))
            ) AS quarter_name,
            COUNT(*) AS matches_played,
            ROUND(AVG(b.runs), 2) AS avg_runs,
            ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY p.player_id, p.player_name, quarter_name
        ORDER BY p.player_name, quarter_name;
    """
}

selected_query = st.selectbox("Choose SQL Query", list(queries.keys()))

st.code(queries[selected_query], language="sql")

if st.button("Run Query"):
    try:
        df = pd.read_sql(queries[selected_query], conn)
        st.write("Rows returned:", len(df))
        st.dataframe(df, width="stretch")
    except Exception as e:
        st.error(e)

st.subheader("Custom SQL Query")

custom_query = st.text_area("Write your own SQL query")

if st.button("Run Custom Query"):
    try:
        custom_df = pd.read_sql(custom_query, conn)
        st.dataframe(custom_df, width="stretch")
    except Exception as e:
        st.error(e)

conn.close()