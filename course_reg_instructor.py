import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class InstructorApprovalView(tk.Tk):
    def __init__(self, instructor_id):
        super().__init__()

        self.title("Instructor Approval View")
        self.state('zoomed')
        self.geometry("800x600")
        self.configure(bg="#00415a")

        self.db_conn = sqlite3.connect("user.db")
        self.cursor = self.db_conn.cursor()
        self.instructor_id = instructor_id

        self.create_widgets()

        self.populate_sections()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use the "clam" theme

        # Configure style for Treeview widget
        self.style.configure("NoBorder.Treeview",
                             background="#00415a",  # Background color
                             foreground="black",  # Font color
                             fieldbackground="#00415a",
                             font=("Helvetica", 12))

        # Configure style for Treeview headings
        self.style.configure("NoBorder.Treeview.Heading",
                             background="#00415a",  # Heading background color
                             foreground="white",  # Heading font color
                             font=("Helvetica", 12, "bold"))

        columns = ("Request ID", "Student ID", "Section ID", "Course Name", "Status")
        self.section_tree = ttk.Treeview(self, columns=columns, show="headings", style="NoBorder.Treeview", height=24)
        self.section_tree.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.85)
        self.section_tree.heading("Request ID", text="Request ID")
        self.section_tree.heading("Student ID", text="Student ID")
        self.section_tree.heading("Section ID", text="Section ID")
        self.section_tree.heading("Course Name", text="Course Name")
        self.section_tree.heading("Status", text="Action")  # Add Status column

        self.section_tree.column("Request ID", width=100)
        self.section_tree.column("Student ID", width=100)
        self.section_tree.column("Section ID", width=100)
        self.section_tree.column("Course Name", width=180)
        self.section_tree.column("Status", width=100)
        
        self.approve_button = tk.Button(self, text="Approve", command=self.approve_section, bg='#87CEEB')
        self.approve_button.place(relx=0.01, rely=0.9, relwidth=0.1, relheight=0.05)

        self.reject_button = tk.Button(self, text="Reject", command=self.reject_section, bg='#87CEEB')
        self.reject_button.place(relx=0.12, rely=0.9, relwidth=0.11, relheight=0.05)

        self.logout_button = tk.Button(self, text="Logout", command=self.logout, bg='#87CEEB')
        self.logout_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)

        self.back_button = tk.Button(self, text="Back", command=self.back, bg='#87CEEB')
        self.back_button.place(relx=0.78, rely=0.9, relwidth=0.1, relheight=0.05)

    def populate_sections(self):
        self.cursor.execute("SELECT course_reg.request_id, course_reg.student_id, section.section_id, course.course_name, course_reg.status FROM course_reg INNER JOIN section ON course_reg.section_id = section.section_id INNER JOIN course ON section.course_id = course.course_id WHERE section.instructor_id = ? AND course_reg.status IN ('r', 'd')", (self.instructor_id,))
        sections = self.cursor.fetchall()
        self.section_tree.delete(*self.section_tree.get_children())
        tag = "even"
        for section in sections:
            status = "Registered" if section[4] == 'r' else "Dropped"
            self.section_tree.insert("", "end", values=section[:4] + (status,), tags=(tag,))
            tag = "odd" if tag == "even" else "even"
        self.section_tree.tag_configure("even", background="#f2f2f2")
        self.section_tree.tag_configure("odd", background="#ffffff")

    def send_email_notification(self, request_id, action):
        try:
            self.cursor.execute("SELECT student_id FROM course_reg WHERE request_id = ?", (request_id,))
            student_id = self.cursor.fetchone()
            if student_id is None:
                messagebox.showerror("Error", "Student ID not found for the given request ID.")
                return
            student_id = student_id[0]

            self.cursor.execute("SELECT first_name, last_name, email FROM users WHERE user_id = ?", (student_id,))
            student_info = self.cursor.fetchone()
            if student_info is None:
                messagebox.showerror("Error", "Student information not found for the given student ID.")
                return
            first_name, last_name, student_email = student_info

            sender_email = "cmuhighscl@gmail.com"  # Your email address
            receiver_email = student_email  # Student's email address

            if action == "Course Registration Request Approved":
                subject = f"Course Registration Approved - {request_id}"
                message = f"Hello {first_name} {last_name},\n\nYour course registration request with Request ID {request_id} has been approved by the instructor.\n\nBest Regards,\nCMU High School"
            elif action == "Course Drop Request Approved":
                subject = f"Course Drop Approved - {request_id}"
                message = f"Hello {first_name} {last_name},\n\nYour course drop request with Request ID {request_id} has been approved by the instructor.\n\nBest Regards,\nCMU High School"
            elif action == "Course Registration Request Rejected":
                subject = f"Course Registration Rejected - {request_id}"
                message = f"Hello {first_name} {last_name},\n\nYour course registration request with Request ID {request_id} has been rejected by the instructor.\n\nBest Regards,\nCMU High School"
            elif action == "Course Drop Request Rejected":
                subject = f"Course Drop Rejected - {request_id}"
                message = f"Hello {first_name} {last_name},\n\nYour course drop request with Request ID {request_id} has been rejected by the instructor.\n\nBest Regards,\nCMU High School"

            # Create message container
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach message
            msg.attach(MIMEText(message, 'plain'))

            # Send email
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
            messagebox.showerror("Error", f"Failed to send email notification: {str(e)}")

    def approve_section(self):
        selected_item = self.section_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No section selected.")
            return

        request_id = self.section_tree.item(selected_item, "values")[0]
        status = self.section_tree.item(selected_item, "values")[4]

        if status == 'Registered':
            self.send_email_notification(request_id, "Course Registration Request Approved")
            self.cursor.execute("UPDATE course_reg SET status = 'y' WHERE request_id = ?", (request_id,))
            messagebox.showinfo("Success", f"Course Registration Request Approved")
            
        elif status == 'Dropped':
            self.send_email_notification(request_id, "Course Drop Request Approved")
            self.cursor.execute("DELETE FROM course_reg WHERE request_id = ?", (request_id,))
            self.cursor.execute("DELETE FROM grade WHERE (student_id, section_id) IN (SELECT student_id, section_id FROM course_reg WHERE request_id = ?)", (request_id,))
            self.cursor.execute("DELETE FROM attendance WHERE (student_id, section_id) IN (SELECT student_id, section_id FROM course_reg WHERE request_id = ?)", (request_id,))
            messagebox.showinfo("Success", f"Drop Request Accepted")
        self.db_conn.commit()
        self.populate_sections()

    def reject_section(self):
        selected_item = self.section_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No section selected.")
            return

        request_id = self.section_tree.item(selected_item, "values")[0]
        status = self.section_tree.item(selected_item, "values")[4]

        if status == 'Registered':
            self.send_email_notification(request_id, "Course Registration Request Rejected")
            self.cursor.execute("DELETE FROM course_reg WHERE request_id = ?", (request_id,))
            messagebox.showinfo("Success", f"Course Registration Request Rejected")
        elif status == 'Dropped':
            self.send_email_notification(request_id, "Course Drop Request Rejected")
            self.cursor.execute("UPDATE course_reg SET status = 'y' WHERE request_id = ?", (request_id,))
            messagebox.showinfo("Success", f"Drop Request Rejected")


        self.db_conn.commit()
        self.populate_sections()
        
    def logout(self):
        self.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\login_register.py'])
        
    def back(self):
        self.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\instructor_dashboard.py', username], check=True)

    def __del__(self):
        self.db_conn.close()

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        username = sys.argv[1]
        print(f"Username received in course_instructor.py: {username}")
    else:
        username = 'kumar1v'
    instructor_id = username  # Specify the instructor ID
    app = InstructorApprovalView(instructor_id)
    app.mainloop()
