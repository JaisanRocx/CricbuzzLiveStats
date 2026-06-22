import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("""
SELECT DISTINCT venue, city
FROM matches
WHERE venue IS NOT NULL
AND venue != ''
""")

rows = cursor.fetchall()

venue_id = 1

for row in rows:

    cursor.execute("""
    INSERT IGNORE INTO venues
    (
        venue_id,
        venue_name,
        city,
        country,
        capacity
    )
    VALUES (%s,%s,%s,%s,%s)
    """,
    (
        venue_id,
        row["venue"],
        row["city"],
        "Unknown",
        0
    ))

    venue_id += 1

conn.commit()

print("Venues inserted:", len(rows))

cursor.close()
conn.close()