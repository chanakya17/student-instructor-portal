import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkcalendar import Calendar
import sys
import subprocess

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#00415a")
        # Connect to SQLite database
        self.conn = sqlite3.connect('user.db')

        # Get instructor ID
        self.instructor_id = instructor_id

        # Section Label
        section_label = tk.Label(root, text="Section:", foreground="white", background="#00415a")
        section_label.place(relx=0.01, rely=0.02)

        # Section Dropdown
        self.section_var = tk.StringVar()
        self.section_dropdown = ttk.Combobox(root, textvariable=self.section_var)
        self.section_dropdown.place(relx=0.08, rely=0.02)
        self.populate_sections_dropdown()  # Populate sections dropdown
        self.section_dropdown.bind("<<ComboboxSelected>>", self.display_students)  # Bind event

        # Date Label
        date_label = tk.Label(root, text="Date:", foreground="white", background="#00415a")
        date_label.place(relx=0.32, rely=0.02)

        # Date Entry
        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, datetime.now().strftime('%m-%d-%Y'))
        self.date_entry.place(relx=0.36, rely=0.02)

        # Calendar Popup Button
        cal_popup_btn = tk.Button(root, text="Select Date", command=self.show_calendar_popup, bg='#87CEEB')
        cal_popup_btn.place(relx=0.55, rely=0.017,relwidth=0.1, relheight=0.05)

        # Attendance Listbox with Checkboxes
        self.attendance_frame = tk.Frame(root, padx=20, pady=20, bg="#00415a")
        self.attendance_frame.place(relx=0.3, rely=0.08, relwidth=0.5, relheight=0.80)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient="vertical")
        self.scrollbar.place(relx=0.98, rely=0.1, relheight=0.75)

        self.canvas = tk.Canvas(self.attendance_frame, bg="#00415a", bd=0, highlightthickness=0, yscrollcommand=self.scrollbar.set)
        self.canvas.place(relx=0.01, rely=0.01, relwidth=0.95, relheight=0.98)
        self.scrollbar.config(command=self.canvas.yview)

        self.inner_frame = tk.Frame(self.canvas, bg="#00415a")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Bind mouse wheel event to canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Submit Attendance Button
        submit_btn = tk.Button(root, text="Submit Attendance", command=self.submit_attendance, bg='#87CEEB')
        submit_btn.place(relx=0.02, rely=0.9, relwidth=0.15, relheight=0.05)

        logout_btn = tk.Button(root, text="Logout", command=self.logout, bg='#87CEEB')
        logout_btn.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)

        back_btn = tk.Button(root, text="Back", command=self.back, bg='#87CEEB')
        back_btn.place(relx=0.78, rely=0.9, relwidth=0.1, relheight=0.05)

        # Automatically display students initially
        self.display_students()

    def show_calendar_popup(self):
        self.calendar_popup = tk.Toplevel(self.root)
        self.calendar_popup.title("Select Date")

        self.cal = Calendar(self.calendar_popup, selectmode="day", date_pattern="mm-dd-yyyy")
        self.cal.pack(padx=10, pady=10)

        select_btn = tk.Button(self.calendar_popup, text="Select", command=self.set_selected_date)
        select_btn.pack(pady=5)

    def set_selected_date(self):
        selected_date = self.cal.get_date()
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, selected_date)
        self.calendar_popup.destroy()

    def populate_sections_dropdown(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT section_id FROM section WHERE instructor_id = ?", (self.instructor_id,))
        sections = cursor.fetchall()
        self.section_dropdown['values'] = [section[0] for section in sections]

    def display_students(self, event=None):
        section_id = self.section_var.get()
        cursor = self.conn.cursor()

        # Fetch students for the selected section
        students = []
        if section_id:
            cursor.execute("SELECT users.user_id, users.first_name, users.last_name FROM course_reg INNER JOIN users ON course_reg.student_id = users.user_id WHERE course_reg.section_id = ? AND course_reg.status = ?", (section_id,'y',))
            students.extend(cursor.fetchall())

            # Clear previous entries
            for widget in self.inner_frame.winfo_children():
                widget.destroy()

            # Display students
            for student in students:
                # Create a frame for each student with a label and a dropdown
                student_frame = tk.Frame(self.inner_frame, bg="#00415a")
                student_frame.pack(fill=tk.X, pady=5)

                student_id = student[0]
                student_label = tk.Label(student_frame, text=f"{student[1]} {student[2]}", width=20, anchor='w', foreground="white", background="#00415a",font=('Arial', 10, 'bold'))
                student_label.pack(side=tk.LEFT, padx=(10, 0))

                status_var = tk.StringVar()
                status_dropdown = ttk.Combobox(student_frame, values=['Present', 'Absent'], textvariable=status_var)
                status_dropdown.pack(side=tk.LEFT, padx=(10, 0))

                # Store student ID as a hidden label
                hidden_label = tk.Label(student_frame, text=student_id, width=5, anchor='w', fg="#00415a", bg=root.cget('bg'))
                hidden_label.pack(side=tk.LEFT)

            self.canvas.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def submit_attendance(self):
        section = self.section_var.get()
        date = self.date_entry.get()

        if section and date:
            cursor = self.conn.cursor()

            for student_frame in self.inner_frame.winfo_children():
                student_id = student_frame.winfo_children()[2].cget("text")
                student_status = student_frame.winfo_children()[1].get()

                if student_status:  # Only insert if status is selected
                    # Get the maximum attendance ID
                    cursor.execute("SELECT MAX(attendance_id) FROM attendance")
                    max_attendance_id = cursor.fetchone()[0]

                    # Increment the attendance ID
                    if max_attendance_id is None:
                        new_attendance_id = 'A10000'  # Start with 'A1000' if there are no existing attendance IDs
                    else:
                    
                        last_id = int(max_attendance_id[1:])  # Extract the numeric part of the last attendance ID
                        new_attendance_id = 'A' + str(last_id + 1) # Increment and format the new attendance ID
                   
                    cursor.execute('INSERT INTO attendance (attendance_id, instructor_id, student_id, section_id, date, status) VALUES (?, ?, ?, ?, ?, ?)',
                                   (new_attendance_id, self.instructor_id, student_id, section, date, student_status))

            self.conn.commit()
            messagebox.showinfo("Success", "Attendance submitted successfully!")
            
    def logout(self):
        self.root.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\login_register.py'])

    def back(self):
        self.root.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\instructor_dashboard.py', username], check=True)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    root.geometry("800x600")
    if len(sys.argv) >= 2:
        username = sys.argv[1]
        print(f"Username received in student_dashboard.py: {username}")
    else:
        username = 'kumar1v'
    instructor_id = username 
    app = AttendanceApp(root)
    root.mainloop()
