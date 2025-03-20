import mysql.connector

# Connect to server
cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="1942002")

# Get a cursor
cur = cnx.cursor()

# Execute a query
# cur.execute("CREATE DATABASE test")
# cur.execute("CREATE DATABASE test_db")
# cur.execute("CREATE DATABASE test_db2")

# Show Databases
cur.execute("SHOW DATABASES")
for db in cur:
    print(db)

# Close connection
cnx.close()