import sys
import os
import time
import requests

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

SCORECARD_URL = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/40381/scard"

HEADERS = {
    "x-rapidapi-key": "56189fe37fmsha58bef222a0c2f2p10741djsn96fd2d678427",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
}

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT match_id FROM matches LIMIT 90")
matches = cursor.fetchall()

saved_matches = 0

for m in matches:
    match_id = m["match_id"]
    print("Fetching scorecard for:", match_id)

    response = requests.get(
        SCORECARD_URL,
        headers=HEADERS,
        params={"matchId": str(match_id)}
    )

    data = response.json()

    if "scorecard" not in data:
        print("No scorecard for", match_id)
        continue

    for innings in data["scorecard"]:

        for batsman in innings.get("batsman", []):
            cursor.execute("""
            INSERT IGNORE INTO players
            (player_id, player_name)
            VALUES (%s,%s)
            """, (
                batsman["id"],
                batsman["name"]
            ))

            cursor.execute("""
            INSERT INTO batting_stats
            (player_id, match_id, runs, balls, fours, sixes, strike_rate)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                batsman["id"],
                match_id,
                batsman.get("runs", 0),
                batsman.get("balls", 0),
                batsman.get("fours", 0),
                batsman.get("sixes", 0),
                float(batsman.get("strkrate", 0))
            ))

        for bowler in innings.get("bowler", []):
            cursor.execute("""
            INSERT IGNORE INTO players
            (player_id, player_name)
            VALUES (%s,%s)
            """, (
                bowler["id"],
                bowler["name"]
            ))

            cursor.execute("""
            INSERT INTO bowling_stats
            (player_id, match_id, overs, maidens, wickets, runs_given, economy)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                bowler["id"],
                match_id,
                float(bowler.get("overs", 0)),
                bowler.get("maidens", 0),
                bowler.get("wickets", 0),
                bowler.get("runs", 0),
                float(bowler.get("economy", 0))
            ))

    conn.commit()
    saved_matches += 1
    time.sleep(1)

print("Scorecards saved for matches:", saved_matches)

cursor.close()
conn.close()