import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        database="simplecode",
        user="root",
        password="xxxx"
    )

