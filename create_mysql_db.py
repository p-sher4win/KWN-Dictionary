import mysql.connector
import os
import re

MASTER_DB = "wordnet_master"
KONKANI_DB = "wordnet_konkani"

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define SQL file paths realtive to script location
konkani_sql_file = os.path.join(script_dir, "wordnet_konkani.sql")
master_sql_file = os.path.join(script_dir, "wordnet_master.sql")

# Define import file function
def import_sql_file(db_name, file_path):
    """Import an SQL file into the MYSQL database"""

    try:
        # Connect to server
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="2002",
            database=db_name
        )

        # Get a cursor
        cur = cnx.cursor()

        # Read and execute the SQL file
        with open(file_path, "r", encoding="utf-8") as file:
            sql_commands = file.read()

            statements = re.split(r';\s*\n', sql_commands) # Split only at semicolon followed by new line

            for command in statements:
                command = command.strip()
                if command:
                    try:
                        cur.execute(command)
                    except mysql.connector.Error as e:
                        print(f"SQL Error: {e} in command:\n{command}\n")

        cnx.commit()
        print(f"Successfully imported {file_path}")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cur.close()
        cnx.close()


# Connect to MYSQL and create the DB
try:
    # Connect to server
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="2002",
    )

    # Get a cursor
    cur = cnx.cursor()

    # Execute create DB query
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {MASTER_DB}")
    print(f"Database '{MASTER_DB}' is ready!")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {KONKANI_DB}")
    print(f"Database '{KONKANI_DB}' is ready!")

except mysql.connector.Error as err:
    print(f"Error: {err}")


finally:
    if 'cnx' in locals() and cnx.is_connected():
        # Close cursor and connection
        cur.close()
        cnx.close()


# Call import sql file function to insert record into WORDNET_DB
import_sql_file(MASTER_DB, master_sql_file)
import_sql_file(KONKANI_DB, konkani_sql_file)

print("\nALL DATABASES ARE ALL SET AND DONE!\n")