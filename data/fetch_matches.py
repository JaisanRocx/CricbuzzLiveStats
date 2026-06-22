import sys
import os
import requests

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

headers = {
    "x-rapidapi-key": "56189fe37fmsha58bef222a0c2f2p10741djsn96fd2d678427",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data = response.json()

conn = get_connection()
cursor = conn.cursor()

inserted_count = 0

for type_match in data["typeMatches"]:
    for series_match in type_match["seriesMatches"]:

        if "seriesAdWrapper" not in series_match:
            continue

        series = series_match["seriesAdWrapper"]
        series_name = series.get("seriesName", "Unknown Series")

        for match in series.get("matches", []):
            match_info = match.get("matchInfo", {})

            match_id = match_info.get("matchId")
            match_desc = match_info.get("matchDesc", "Unknown")
            match_format = match_info.get("matchFormat", "Unknown")
            status = match_info.get("status", "Unknown")
            start_date = match_info.get("startDate", 0)

            team1 = match_info.get("team1", {}).get("teamName", "Unknown")
            team2 = match_info.get("team2", {}).get("teamName", "Unknown")

            venue_info = match_info.get("venueInfo", {})
            venue = venue_info.get("ground", "Unknown")
            city = venue_info.get("city", "Unknown")

            if match_id is None:
                continue

            cursor.execute("""
            INSERT IGNORE INTO matches
            (
                match_id,
                series_name,
                match_desc,
                match_format,
                team1,
                team2,
                venue,
                city,
                status,
                start_date
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                match_id,
                series_name,
                match_desc,
                match_format,
                team1,
                team2,
                venue,
                city,
                status,
                start_date
            ))

            inserted_count += cursor.rowcount

conn.commit()

print(f"Matches inserted successfully: {inserted_count}")

cursor.close()
conn.close()