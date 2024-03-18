import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")

        # Connect to SQLite database
        self.conn = sqlite3.connect('attendance.db')
        self.create_table()

        # Section Dropdown
        self.section_var = tk.StringVar()
        sections = ['A', 'B', 'C']  # Add your sections here
        self.section_dropdown = ttk.Combobox(root, values=sections, textvariable=self.section_var, state="readonly")
        self.section_dropdown.grid(row=0, column=0, padx=10, pady=10)
        self.section_dropdown.bind("<<ComboboxSelected>>", self.update_student_dropdown)

        # Date Entry
        self.date_label = tk.Label(root, text="Date:")
        self.date_label.grid(row=0, column=1, padx=10, pady=10)
        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=0, column=2, padx=10, pady=10)

        # Student Dropdown for Checking Attendance
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(root, textvariable=self.student_var, state="readonly")
        self.student_dropdown.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Check Attendance Button
        check_attendance_btn = tk.Button(root, text="Check Your Attendance", command=self.check_attendance)
        check_attendance_btn.grid(row=2, column=0, columnspan=4, pady=10)

        # Attendance Text Widget
        self.attendance_text = tk.Text(root, wrap=tk.WORD, height=10, width=50)
        self.attendance_text.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        # Print Attendance Button
        print_attendance_btn = tk.Button(root, text="Print Attendance", command=self.print_attendance)
        print_attendance_btn.grid(row=4, column=0, columnspan=4, pady=10)

        # Attendance Status Label
        self.attendance_status_label = tk.Label(root, text="")
        self.attendance_status_label.grid(row=5, column=0, columnspan=4, pady=10)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                section TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                section TEXT NOT NULL,
                status TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_sample_data(self):
        student_data = [
            ("John Doe", "A"),
            # ... (other student data)
        ]

        cursor = self.conn.cursor()
        cursor.executemany('INSERT INTO students (name, section) VALUES (?, ?)', student_data)
        self.conn.commit()
        messagebox.showinfo("Success", "Sample data inserted successfully!")

    def update_student_dropdown(self, event):
        section = self.section_var.get()
        if section:
            cursor = self.conn.cursor()
            cursor.execute('SELECT name FROM students WHERE section=?', (section,))
            students = cursor.fetchall()

            self.student_dropdown['values'] = [student[0] for student in students]
            self.student_var.set("")  # Clear selection

    def check_attendance(self):
        student_name = self.student_var.get()
        if student_name:
            cursor = self.conn.cursor()
            cursor.execute('SELECT date, status FROM attendance WHERE name=?', (student_name,))
            attendance_data = cursor.fetchall()

            # Display attendance data in the text widget
            if attendance_data:
                status_text = f"Attendance for {student_name}:\n"
                for date, status in attendance_data:
                    status_text += f"{date}: {status}\n"
                self.attendance_text.delete(1.0, tk.END)  # Clear previous entries
                self.attendance_text.insert(tk.END, status_text)
            else:
                self.attendance_text.delete(1.0, tk.END)  # Clear previous entries
                self.attendance_text.insert(tk.END, f"No attendance data found for {student_name}")

    def print_attendance(self):
        print("print attendence")



if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)

    
    # app.insert_sample_data()

    root.mainloop()
