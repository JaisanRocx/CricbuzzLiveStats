import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jaisan@23",
        database="cricbuzz"
    )