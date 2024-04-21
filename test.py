import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

try:
    # Fetch all rows where the role is 'student'
    cursor.execute("SELECT user_id FROM users WHERE role = 'Student'")
    student_ids = cursor.fetchall()
    print(student_ids)
    # Update class for each student
    for student_id_tuple in student_ids:
        student_id = student_id_tuple[0]  # Extract student_id from the tuple
        # Generate a random class value between 9 and 12 for each student
        random_class = random.randint(9, 12)

        # Update the class for the current student
        cursor.execute("UPDATE users SET class = ? WHERE user_id = ?", (random_class, student_id))

    # Commit the transaction
    conn.commit()

    print("Class updated successfully.")

except sqlite3.Error as e:
    print("Error occurred:", e)

finally:
    # Close the database connection
    conn.close()
