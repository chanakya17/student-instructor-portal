
import tkinter as tk
from tkinter import ttk,messagebox
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
        sections = ['A', 'B', 'C']  
        self.section_dropdown = ttk.Combobox(root, values=sections, textvariable=self.section_var)
        self.section_dropdown.grid(row=0, column=0, padx=10, pady=10)

        # Date Entry
        self.date_label = tk.Label(root, text="Date:")
        self.date_label.grid(row=0, column=1, padx=10, pady=10)
        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=0, column=2, padx=10, pady=10)

        # Display Students Button
        display_btn = tk.Button(root, text="Display Students", command=self.display_students)
        display_btn.grid(row=0, column=3, padx=10, pady=10)

        # Attendance Listbox with Checkboxes
        self.attendance_frame = tk.Frame(root,  padx=20, pady=20)
        self.attendance_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Scrollbar
        # self.scroll_bar = tk.Scrollbar(root)
        # self.scroll_bar.grid(row=1, column=4, sticky=tk.NS)
        # self.attendance_listbox.config(yscrollcommand=self.scroll_bar.set)
        # self.scroll_bar.config(command=self.attendance_listbox.yview)

        # Submit Attendance Button
        submit_btn = tk.Button(root, text="Submit Attendance", command=self.submit_attendance)
        submit_btn.grid(row=2, column=0, columnspan=4, pady=10)

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

    def display_students(self):
        section = self.section_var.get()
        if section:
            cursor = self.conn.cursor()
            cursor.execute('SELECT name FROM students WHERE section=?', (section,))
            students = cursor.fetchall()

            # Clear previous entries
            for widget in self.attendance_frame.winfo_children():
                widget.destroy()
            

            for student in students:
                # Create a frame for each student with a label and a dropdown
                student_frame = tk.Frame(self.attendance_frame)
                student_frame.pack(fill=tk.X, pady=2)

                student_label = tk.Label(student_frame, text=student[0], width=20, anchor='w')
                student_label.pack(side=tk.LEFT, padx=(10, 0))

                status_var = tk.StringVar()
                status_dropdown = ttk.Combobox(student_frame, values=['Present', 'Absent'], textvariable=status_var)
                status_dropdown.pack(side=tk.LEFT, padx=(10, 0))

    def submit_attendance(self):
        section = self.section_var.get()
        date = self.date_entry.get()

        if section and date:
            cursor = self.conn.cursor()

            for index, student_frame in enumerate(self.attendance_frame.winfo_children()):
                student_name = student_frame.winfo_children()[0].cget("text")
                status = student_frame.winfo_children()[1].get()

                if status:  # Only insert if status is selected
                    cursor.execute('INSERT INTO attendance (name, section, status, date) VALUES (?, ?, ?, ?)',
                                   (student_name, section, status, date))

            self.conn.commit()
            messagebox.showinfo("Success", "Attendance submitted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
