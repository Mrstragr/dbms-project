import os
os.system("cls")

import mysql.connector as db

# This function creates and returns a connection object that you can reuse everywhere.
def create_connection():
    connection = None

    try:
        connection = db.connect(
            host="localhost",
            user="root",        
            password="ansh.kumar@02",  
            database="sau_lab_management"       
        )

        if connection.is_connected():
            print("✅ Connection successful!")
        return connection
    
    except db.Error as err:
        print(f"❌ Error: {err}")
        return None
    

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connection closed!")



