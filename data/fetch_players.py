import sys
import os
import time
import requests

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

URL_TEMPLATE = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{}"

HEADERS = {
    "x-rapidapi-key": "YOUR_API_KEY",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("""
SELECT player_id
FROM players
""")

players = cursor.fetchall()

updated = 0

for player in players:

    player_id = player["player_id"]

    try:
        url = URL_TEMPLATE.format(player_id)

        response = requests.get(
            url,
            headers=HEADERS
        )

        data = response.json()

        player_name = data.get("name", "")
        country = data.get("intlTeam", "")

        role = data.get("role", "")

        batting_style = data.get("bat", "")
        bowling_style = data.get("bowl", "")

        cursor.execute("""
        UPDATE players
        SET
            player_name=%s,
            country=%s,
            role=%s,
            batting_style=%s,
            bowling_style=%s
        WHERE player_id=%s
        """,
        (
            player_name,
            country,
            role,
            batting_style,
            bowling_style,
            player_id
        ))

        conn.commit()

        updated += 1

        print(f"Updated player {player_id}")

        time.sleep(1)

    except Exception as e:
        print(f"Failed for player {player_id}: {e}")

print(f"\nPlayers updated: {updated}")

cursor.close()
conn.close()