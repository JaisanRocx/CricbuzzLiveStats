import sys
import os
import requests

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/40381/scard"

headers = {
    "x-rapidapi-key": "YOUR_API_KEY",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

querystring = {
    "matchId": "40381"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

conn = get_connection()
cursor = conn.cursor()

match_id = 40381

cursor.execute("""
INSERT IGNORE INTO matches
(match_id, series_name, match_desc, match_format, team1, team2, venue, city, status, start_date)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""",
(
    match_id,
    "Demo Series",
    "Demo Match",
    "T20",
    "Team A",
    "Team B",
    "Demo Venue",
    "Demo City",
    "Completed",
    0
))

for bowler in data["scorecard"][0]["bowler"]:

    cursor.execute("""
    INSERT IGNORE INTO players
    (player_id, player_name)
    VALUES (%s,%s)
    """,
    (
        bowler["id"],
        bowler["name"]
    ))

    cursor.execute("""
    INSERT INTO bowling_stats
    (player_id, match_id, overs, maidens, wickets, runs_given, economy)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        bowler["id"],
        match_id,
        float(bowler["overs"]),
        bowler["maidens"],
        bowler["wickets"],
        bowler["runs"],
        float(bowler["economy"])
    ))

conn.commit()

print("Bowling data inserted successfully!")

cursor.close()
conn.close()