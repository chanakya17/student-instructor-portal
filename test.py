import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('user.db')

# Create a cursor object
c = conn.cursor()
student_id = 'ander1e'
courses = c.execute('''SELECT course_name 
                    FROM course 
                    JOIN section ON course.course_id = section.course_id 
                    JOIN course_reg ON section.section_id = course_reg.section_id 
                    WHERE course_reg.student_id=? AND course_reg.status = 'y' ''', (student_id,)).fetchall()

print(courses[0])