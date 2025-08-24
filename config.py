# config.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2225",         # Apna MySQL password yahan daal
        database="office"
    )
