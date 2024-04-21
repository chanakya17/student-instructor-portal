import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import sqlite3
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class RegisteredCoursesView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Registered Courses View")
        self.state('zoomed')
        self.geometry("1000x600")
        self.configure(bg="#00415a")

        self.db_conn = sqlite3.connect("user.db")
        self.cursor = self.db_conn.cursor()

        self.create_widgets()

        
        if len(sys.argv) >= 2:
            self.student_id = sys.argv[1]
            print(f"Username received in student_course_view.py: {self.student_id}")
        else:
            self.student_id = 'raoch2c'

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

        self.section_tree = ttk.Treeview(self, columns=("Section ID", "Course Name", "Instructor", "Start Time", "End Time", "Class Room", "Status"), show="headings", height=24, style="NoBorder.Treeview")
        self.section_tree.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.85)

        self.section_tree.heading("Section ID", text="Section ID")
        self.section_tree.heading("Course Name", text="Course Name")
        self.section_tree.heading("Instructor", text="Instructor")
        self.section_tree.heading("Start Time", text="Start Time")
        self.section_tree.heading("End Time", text="End Time")
        self.section_tree.heading("Class Room", text="Class Room")
        self.section_tree.heading("Status", text="Status")  # Add Status column

        self.drop_button = tk.Button(self, text="Drop Section", command=self.drop_section, bg='#87CEEB')
        self.drop_button.place(relx=0.01, rely=0.9, relwidth=0.1, relheight=0.05)

        self.register_button = tk.Button(self, text="Register Courses", command=self.register_section, bg='#87CEEB')
        self.register_button.place(relx=0.12, rely=0.9, relwidth=0.11, relheight=0.05)

        self.print_button = tk.Button(self, text="Print", command=self.generate_pdf, bg='#87CEEB')
        self.print_button.place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.05)

        self.back_button = tk.Button(self, text="Back", command=self.back, bg='#87CEEB')
        self.back_button.place(relx=0.78, rely=0.9, relwidth=0.1, relheight=0.05)

        self.logout_button = tk.Button(self, text="Logout", command=self.logout, bg='#87CEEB')
        self.logout_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)

    def populate_sections(self):
        self.cursor.execute("SELECT section.section_id, course.course_name, users.first_name || ' ' || users.last_name, section.start_time, section.end_time, section.class_room, course_reg.status FROM section INNER JOIN course_reg ON section.section_id = course_reg.section_id INNER JOIN course ON section.course_id = course.course_id INNER JOIN users ON section.instructor_id = users.user_id WHERE course_reg.student_id = ? and (course_reg.status = 'y' OR course_reg.status = 'd')", (self.student_id,))
        sections = self.cursor.fetchall()
        self.section_tree.delete(*self.section_tree.get_children())
        tag = "even"
        for section in sections:
            status = "Registered" if section[6] == 'y' else "Dropped"
            self.section_tree.insert("", "end", values=section[:6] + (status,), tags=(tag,))
            tag = "odd" if tag == "even" else "even"
        self.section_tree.tag_configure("even", background="#f2f2f2")
        self.section_tree.tag_configure("odd", background="#ffffff")

    def drop_section(self):
        selected_item = self.section_tree.selection()
        if not selected_item:
            print("Error: No section selected.")
            return

        section_id = self.section_tree.item(selected_item, "values")[0]
        self.cursor.execute("SELECT request_id, status, instructor_id FROM course_reg INNER JOIN section ON course_reg.section_id = section.section_id WHERE section.section_id = ? AND course_reg.student_id = ?", (section_id, self.student_id))
        result = self.cursor.fetchone()

        if result:
            request_id, status, instructor_id = result
            if status == 'd':
                messagebox.showerror("Section Already Dropped", "The section is already dropped. Please wait for instructor confirmation.")
            else:
                # Update course registration status to 'd' (dropped)
                self.cursor.execute("UPDATE course_reg SET status = 'd' WHERE request_id = ?", (request_id,))
                self.db_conn.commit()
                
                # Retrieve instructor's email
                self.cursor.execute("SELECT email FROM users WHERE user_id = ?", (instructor_id,))
                instructor_email = self.cursor.fetchone()[0]
                
                # Send email notification to the instructor
                self.send_email_to_instructor(instructor_email, section_id, request_id)
                messagebox.showinfo("Success", f"Drop Request Sent")
                # Repopulate sections
                self.populate_sections()
        else:
            print("Error: Request ID not found")

    def send_email_to_instructor(self, instructor_email, section_id, request_id):
        try:
            sender_email = ""  # Your email address
            receiver_email = instructor_email  # Instructor's email address
            subject = f"Course Drop Request: {section_id}"
            message = f"New Course Drop Request\n\nRequest ID: {request_id}\nSection ID: {section_id}.\n\n\nBest Regards,\nYour School Name"

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
            smtp_password = ""  # Your SMTP password

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
        except Exception as e:
            print("Failed to send email:", e)

    def register_section(self):
        print('register')
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\Course_reg_student.py', self.student_id], check=True)
        print("Logout button clicked")

    def generate_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        # Fetch student name
        self.cursor.execute("SELECT first_name, last_name FROM users WHERE user_id = ?", (self.student_id,))
        name = self.cursor.fetchone()
        student_name = " ".join(name) if name else "Unknown"

        content = []

        
        title_style = getSampleStyleSheet()["Title"]

        
        normal_style = getSampleStyleSheet()["Normal"]

        
        content.append(Paragraph("Registered Courses Report", title_style))

        
        content.append(Paragraph(f"Student Name: {student_name}", normal_style))

       
        table_data = [["Section ID", "Course Name", "Instructor", "Start Time", "End Time", "Class Room", "Status"]]
        for item in self.section_tree.get_children():
            values = self.section_tree.item(item, "values")
            table_data.append(values)

        
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]

        
        table = Table(table_data, colWidths=[50, 120, 120, 120, 120, 60, 80])
        table.setStyle(TableStyle(table_style))
        content.append(table)

        
        pdf_file = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
        pdf_file.pagesize = (letter[1], letter[0])  # Swap width and height for landscape
        pdf_file.build(content)

        messagebox.showinfo("Success", "PDF generated successfully.")

    def logout(self):
        self.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\login_register.py'])

    def back(self):
        self.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\student_dashboard.py', self.student_id], check=True)

    def __del__(self):
        self.db_conn.close()

if __name__ == "__main__":
    app = RegisteredCoursesView()
    app.mainloop()
