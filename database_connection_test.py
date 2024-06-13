#database_connection_test.py

import mysql.connector

# Replace the placeholders with your actual database credentials
USER = "root"
PASSWORD = "weststar@ad123#"
HOST = "192.168.1.10"
DB = "gksbdb"

# Establish a connection to the MySQL database
try:
    cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DB)
    print("Connected")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    # Handle the error gracefully

# Close the connection
if cnx.is_connected():
    cnx.close()
    print("Connection closed")
