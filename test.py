import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Query the sqlite_master table to check for the existence of the 'users' table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
table_exists = cursor.fetchone() is not None


# Check if the 'users' table exists
if table_exists:
    print("The 'users' table exists in the database.")
    
    # Execute a SELECT query to retrieve all users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    if users:
        print("List of Users:")
        for user in users:
            print(f"User ID: {user[0]}")
            print(f"Username: {user[1]}")
            print(f"Email: {user[2]}")
            print("--------------------")
    else:
         print("No users found in the database.")

else:
    print("The 'users' table does not exist in the database.")

# Close the cursor and connection
cursor.close()
conn.close()