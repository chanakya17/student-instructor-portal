import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('user.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define the table name to be deleted
table_name = 'course'

# Execute the SQL command to drop the table
drop_table_query = f'DROP TABLE IF EXISTS {table_name};'
cursor.execute(drop_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()
