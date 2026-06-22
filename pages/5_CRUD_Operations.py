import sys
import os
import streamlit as st
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_connection import get_connection

st.title("🛠️ CRUD Operations - Players")

conn = get_connection()
cursor = conn.cursor()

menu = st.sidebar.radio(
    "Choose Operation",
    ["View Players", "Add Player", "Update Player", "Delete Player"]
)

if menu == "View Players":
    st.subheader("All Players")

    df = pd.read_sql("SELECT * FROM players LIMIT 100", conn)
    st.dataframe(df, width="stretch")

elif menu == "Add Player":
    st.subheader("Add New Player")

    player_id = st.number_input("Player ID", min_value=1, step=1)
    player_name = st.text_input("Player Name")
    country = st.text_input("Country")
    role = st.text_input("Role")
    batting_style = st.text_input("Batting Style")
    bowling_style = st.text_input("Bowling Style")

    if st.button("Add Player"):
        try:
            cursor.execute("""
            INSERT INTO players
            (player_id, player_name, country, role, batting_style, bowling_style)
            VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                player_id,
                player_name,
                country,
                role,
                batting_style,
                bowling_style
            ))

            conn.commit()
            st.success("Player added successfully!")

        except Exception as e:
            st.error(e)

elif menu == "Update Player":
    st.subheader("Update Player")

    player_id = st.number_input("Enter Player ID to Update", min_value=1, step=1)
    player_name = st.text_input("New Player Name")
    country = st.text_input("New Country")
    role = st.text_input("New Role")
    batting_style = st.text_input("New Batting Style")
    bowling_style = st.text_input("New Bowling Style")

    if st.button("Update Player"):
        try:
            cursor.execute("""
            UPDATE players
            SET player_name=%s,
                country=%s,
                role=%s,
                batting_style=%s,
                bowling_style=%s
            WHERE player_id=%s
            """, (
                player_name,
                country,
                role,
                batting_style,
                bowling_style,
                player_id
            ))

            conn.commit()
            st.success("Player updated successfully!")

        except Exception as e:
            st.error(e)

elif menu == "Delete Player":
    st.subheader("Delete Player")

    player_id = st.number_input("Enter Player ID to Delete", min_value=1, step=1)

    if st.button("Delete Player"):
        try:
            cursor.execute(
                "DELETE FROM players WHERE player_id=%s",
                (player_id,)
            )

            conn.commit()
            st.success("Player deleted successfully!")

        except Exception as e:
            st.error(e)

cursor.close()
conn.close()