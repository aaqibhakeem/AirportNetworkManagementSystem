import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="<hostname>",             # Replace with your MySQL host
        user="<username>",             # Replace with your MySQL user
        password="<password>",         # Replace with your MySQL password
        database="<database_name>"           # Replace with your MySQL database name
    )