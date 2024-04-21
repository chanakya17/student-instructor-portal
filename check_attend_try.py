import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import sys
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

class StudentAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Checker")
        self.root.geometry("800x600")
        self.root.configure(bg="#00415a")
        # Connect to SQLite database
        self.conn = sqlite3.connect('user.db')

        # Get student ID
        self.student_id = username


        # Label to display full name
        self.full_name_display_label = tk.Label(root, text="", font=('Arial', 14, 'bold'), bg="#00415a", fg="white")
        self.full_name_display_label.place(relx=0.1, rely=0.025)
        cursor = self.conn.cursor()
        cursor.execute("SELECT first_name, last_name FROM users WHERE user_id = ?", (self.student_id,))
        full_name = cursor.fetchone()
        if full_name:
            self.full_name_display_label.config(text=f" {full_name[0]} {full_name[1]}")

        # Section Label
        section_label = tk.Label(root, text="Section:", font=('Arial', 14, 'bold'), bg="#00415a", fg="white")
        section_label.place(relx=0.4, rely=0.02)

        # Section Dropdown
        self.section_var = tk.StringVar()
        self.section_dropdown = ttk.Combobox(root, textvariable=self.section_var, width=25)
        self.section_dropdown.place(relx=0.48, rely=0.025)

        # Display Attendance Button
        display_btn = tk.Button(root, text="Display Attendance", command=self.display_attendance, bg='#87CEEB')
        display_btn.place(relx=0.8, rely=0.02,relwidth=0.1, relheight=0.05)

        # Print Attendance Button
        print_btn = tk.Button(root, text="Print", command=self.generate_pdf, bg='#87CEEB')
        print_btn.place(relx=0.5, rely=0.9,relwidth=0.1, relheight=0.05)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#00415a", fieldbackground="#00415a", font=("Arial", 12))
        # Configure style for Treeview headings
        self.style.configure("Treeview.Heading",
                             background="#00415a",  # Heading background color
                             foreground="white",  # Heading font color
                             font=("Helvetica", 12, "bold"))  # Heading font
        # Attendance Treeview
        self.attendance_tree = ttk.Treeview(root, columns=('Date', 'Status'), show="headings", height=18)
        self.attendance_tree.heading('Date', text='Date')
        self.attendance_tree.heading('Status', text='Status')
        self.attendance_tree.column('Date', width=150)
        self.attendance_tree.column('Status', width=150)
        self.attendance_tree.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.7)

        # Back Button
        self.back_button = tk.Button(root, text="Back", command=self.back, bg='#87CEEB')
        self.back_button.place(relx=0.78, rely=0.9, relwidth=0.1, relheight=0.05)

        # Logout Button
        self.logout_button = tk.Button(root, text="Logout", command=self.logout, bg='#87CEEB')
        self.logout_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)

    def populate_sections_dropdown(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT section_id FROM course_reg WHERE student_id = ? AND (status='y' OR status='d')", (self.student_id,))
        sections = cursor.fetchall()
        self.section_dropdown['values'] = [section[0] for section in sections]

    def display_attendance(self):
        section_id = self.section_var.get()
        cursor = self.conn.cursor()

        # Fetch section details
        cursor.execute("SELECT course_name FROM section JOIN course ON section.course_id = course.course_id WHERE section_id = ?", (section_id,))
        section_details = cursor.fetchone()

        # Fetch attendance for the selected section and student
        cursor.execute("SELECT date, status FROM attendance WHERE student_id = ? AND section_id = ?", (self.student_id, section_id))
        attendance_data = cursor.fetchall()

        # Clear previous entries
        self.attendance_tree.delete(*self.attendance_tree.get_children())
        tag = "even"
        # Display attendance
        for date, status in attendance_data:
            self.attendance_tree.insert('', 'end', values=(date, status), tags=(tag,))
            tag = "odd" if tag == "even" else "even"
        self.attendance_tree.tag_configure("even", background="#f2f2f2")
        self.attendance_tree.tag_configure("odd", background="#ffffff")

    def generate_pdf(self):
        # Prompt user to select a file location to save the PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return  # User canceled operation or provided invalid file path

        # Retrieve student details
        cursor = self.conn.cursor()
        cursor.execute("SELECT first_name, last_name FROM users WHERE user_id = ?", (self.student_id,))
        student_name = " ".join(cursor.fetchone())

        section_id = self.section_var.get()

        # Fetch section details
        cursor.execute("SELECT course_name FROM section JOIN course ON section.course_id = course.course_id WHERE section_id = ?", (section_id,))
        section_details = cursor.fetchone()

        # Fetch attendance for the selected section and student
        cursor.execute("SELECT date, status FROM attendance WHERE student_id = ? AND section_id = ?", (self.student_id, section_id))
        attendance_data = cursor.fetchall()

        # Create a PDF document
        pdf_file = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()

        # Content for the PDF
        content = []

        # Title
        title_style = styles["Title"]
        title = Paragraph("Student Attendance Report", title_style)
        content.append(title)

        # Student Details
        student_details = f"Student Name: {student_name}\nSection ID: {section_id}\nCourse Name: {section_details[0]}\n\n"
        student_details_paragraph = Paragraph(student_details, styles["Normal"])
        content.append(student_details_paragraph)

        # Attendance Data
        table_data = [["Date", "Status"]]
        for date, status in attendance_data:
            table_data.append([date, status])

        # Table Header and Data
        table = Table(table_data, colWidths=[200, 200])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        content.append(table)

        # Build PDF
        pdf_file.build(content)

        messagebox.showinfo("Success", "PDF generated successfully.")

    def logout(self):
        self.root.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\login_register.py'])

    def back(self):
        self.root.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\student_dashboard.py', username], check=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    root.configure(bg="#00415a")
    if len(sys.argv) >= 2:
        username = sys.argv[1]
        print(f"Username received in student_attendance.py: {username}")
    else:
        username = 'musuk2s'
    app = StudentAttendanceApp(root)
    app.populate_sections_dropdown()  # Populate sections dropdown
    root.mainloop()
