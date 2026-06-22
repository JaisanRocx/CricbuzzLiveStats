import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("""
SELECT DISTINCT series_name
FROM matches
WHERE series_name IS NOT NULL
AND series_name != ''
""")

rows = cursor.fetchall()

for row in rows:
    cursor.execute("""
    INSERT IGNORE INTO series (series_name)
    VALUES (%s)
    """, (row["series_name"],))

conn.commit()

print("Series inserted:", len(rows))

cursor.close()
conn.close()