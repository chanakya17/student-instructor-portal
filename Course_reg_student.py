import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class RegisterSectionsPage(tk.Tk):
    def __init__(self, student_id):
        super().__init__()
        self.title("Register Sections")
        self.geometry("900x600")
        self.state('zoomed')
        self.student_id = student_id
        self.configure(bg="#00415a") 

        self.db_conn = sqlite3.connect("user.db")
        self.cursor = self.db_conn.cursor()

        self.create_widgets()
        self.populate_sections()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use the "clam" theme

        # Configure style for Treeview widget
        self.style.configure("Treeview",
                             background="#00415a",  # Background color
                             foreground="black",  # Font color
                             fieldbackground="#00415a",
                             font=("Helvetica", 12))  # Field background color

        # Configure style for Treeview headings
        self.style.configure("Treeview.Heading",
                             background="#00415a",  # Heading background color
                             foreground="white",  # Heading font color
                             font=("Helvetica", 12, "bold"))  # Heading font

        self.section_tree = ttk.Treeview(self, columns=("Section ID", "Course Name", "Instructor", "Start Time", "End Time", "Class Room"), show="headings", height=24)
        self.section_tree.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.85)

        self.section_tree.heading("Section ID", text="Section ID")
        self.section_tree.heading("Course Name", text="Course Name")
        self.section_tree.heading("Instructor", text="Instructor")
        self.section_tree.heading("Start Time", text="Start Time")
        self.section_tree.heading("End Time", text="End Time")
        self.section_tree.heading("Class Room", text="Class Room")

        self.section_tree.column("Section ID", width=110)
        self.section_tree.column("Course Name", width=180)
        self.section_tree.column("Instructor", width=200)
        self.section_tree.column("Start Time", width=180)
        self.section_tree.column("End Time", width=180)
        self.section_tree.column("Class Room", width=110)

        self.register_button = tk.Button(self, text="Register", command=self.register_section, bg='#87CEEB')
        self.register_button.place(relx=0.01, rely=0.9, relwidth=0.1, relheight=0.05)

        self.back_button = tk.Button(self, text="Back", command=self.back, bg='#87CEEB')
        self.back_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)

    def populate_sections(self):
        self.cursor.execute("SELECT section.section_id, course.course_name, users.first_name || ' ' || users.last_name, section.start_time, section.end_time, section.class_room FROM section \
            LEFT JOIN course_reg ON section.section_id = course_reg.section_id AND course_reg.student_id = ? \
            INNER JOIN course ON section.course_id = course.course_id \
            INNER JOIN users ON section.instructor_id = users.user_id \
            INNER JOIN users AS u ON u.user_id = ? AND course.class = u.class \
            WHERE course_reg.student_id IS NULL \
            AND section.course_id NOT IN (SELECT section.course_id FROM section \
                                            INNER JOIN course_reg ON section.section_id = course_reg.section_id \
                                            WHERE course_reg.student_id = ?) \
            ORDER BY section.section_id ", (self.student_id, self.student_id, self.student_id))

        sections = self.cursor.fetchall()
        self.section_tree.delete(*self.section_tree.get_children())
        tag = "even"
        for section in sections:
            self.section_tree.insert("", "end", values=section, tags=(tag,))
            tag = "odd" if tag == "even" else "even"
        self.section_tree.tag_configure("even", background="#f2f2f2")
        self.section_tree.tag_configure("odd", background="#ffffff")

    def generate_request_id(self):
        # Retrieve the maximum Request ID
        max_request_id_result = self.cursor.execute("SELECT MAX(request_id) FROM course_reg").fetchone()
        if max_request_id_result is None or max_request_id_result[0] is None:
            new_request_id = 'R1000'  
        else:
            max_request_id = max_request_id_result[0]
            last_id = int(max_request_id[1:]) 
            new_request_id = 'R' + str(last_id + 1) 
        return new_request_id

    def send_email_to_instructor(self, instructor_email,course_name,section_id,request_id,student_name):
        try:
            sender_email = "cmuhighscl@gmail.com"  # Your email address
            receiver_email = instructor_email  # Instructor's email address
            subject = f"Course Registration Request: {request_id}"
            message = f"New Course Registration Request\n\nRequest ID: {request_id}\nCourse: {course_name}\nSection: {section_id}\nStudent Name: {student_name}\n\nBest Regards,\nCMU High School"

           
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

           
            msg.attach(MIMEText(message, 'plain'))

            
            smtp_server = "smtp.gmail.com"  # Your SMTP server address
            smtp_port = 587  # Your SMTP port
            smtp_username = sender_email  # Your SMTP username
            smtp_password = "oixlkevvlbobqicl"  # Your SMTP password

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
        except Exception as e:
            print("Failed to send email:", e)

    def register_section(self):
        selected_section = self.section_tree.focus()
        if selected_section:
            section_info = self.section_tree.item(selected_section, "values")
            section_id = section_info[0]
            course_name = section_info[1]
            
            # Retrieve the instructor's email by joining the section and users tables
            self.cursor.execute("SELECT users.email FROM section INNER JOIN users ON section.instructor_id = users.user_id WHERE section.section_id = ?", (section_id,))
            instructor_email = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT first_name||' ' ||last_name FROM users WHERE user_id = ?", (self.student_id,))
            student_name = self.cursor.fetchone()[0]
            print(instructor_email)
            request_id=self.generate_request_id()
            # Insert the record into the database
            self.cursor.execute("INSERT INTO course_reg (request_id, student_id, section_id, status) VALUES (?, ?, ?, 'r')", (request_id, self.student_id, section_id))
            self.db_conn.commit()
            self.populate_sections()
            self.send_email_to_instructor(instructor_email,course_name, section_id,request_id,student_name)

    def back(self):
        self.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\course_view_student.py', self.student_id], check=True)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        username = sys.argv[1]
        print(f"Username received in student_dashboard.py: {username}")
    else:
        username = 'raoch2c'
    student_id = username

    app = RegisterSectionsPage(student_id)
    app.mainloop()
