import sqlite3

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('user.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define your table schema and create the table
table_creation_query = '''
CREATE TABLE IF NOT EXISTS notification (
    notification_id TEXT PRIMARY KEY,
    receiver_id TEXT,
    msg_text TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    msg_status TEXT
);
'''

cursor.execute(table_creation_query)

# Commit the changes and close the connection
conn.commit()
conn.close()



# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('user.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define your table schema and create the table
table_creation_query = '''
CREATE TABLE IF NOT EXISTS grade (
    student_id TEXT,
    course_id TEXT,
    grade TEXT
);
'''

cursor.execute(table_creation_query)

# Commit the changes and close the connection
conn.commit()
conn.close()