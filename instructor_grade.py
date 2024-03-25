import tkinter as tk
from tkinter import ttk, messagebox
import sys
import sqlite3

class InstructorGradeApp:
    def __init__(self, root, instructor_id):
        self.root = root
        self.root.title("Instructor Grade Management")

        # Connect to SQLite3 database
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()

        self.instructor_id = instructor_id

        self.create_widgets()

    def create_widgets(self):
        self.section_label = tk.Label(self.root, text="Select Section:")
        self.section_label.grid(row=0, column=0, padx=5, pady=5)
        self.section_var = tk.StringVar()
        self.section_combobox = ttk.Combobox(self.root, textvariable=self.section_var, state="readonly")
        self.section_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.student_grades_frame = tk.Frame(self.root)
        self.student_grades_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.add_grades_button = tk.Button(self.root, text="Add Grades", command=self.add_grades)
        self.add_grades_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Populate section dropdown
        self.populate_section_dropdown()
        self.section_combobox.bind("<<ComboboxSelected>>", self.load_students)

    def populate_section_dropdown(self):
        try:
            sections = self.c.execute("SELECT section_id FROM section WHERE instructor_id=?", (self.instructor_id,)).fetchall()
            self.section_combobox["values"] = [section[0] for section in sections]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching sections: {e}")

    def load_students(self, event):
        section_id = self.section_var.get()
        if not section_id:
            messagebox.showerror("Error", "Please select a section.")
            return

        try:
            self.students = self.c.execute("SELECT users.first_name, users.last_name, course_reg.student_id FROM users, course_reg WHERE course_reg.student_id = users.user_id AND course_reg.section_id=? AND users.role= 'Student' AND course_reg.status='y'", (section_id,)).fetchall()

            for i, student in enumerate(self.students):
                student_name = f"{student[0]} {student[1]}"
                student_label = tk.Label(self.student_grades_frame, text=student_name)
                student_label.grid(row=i, column=0, padx=5, pady=5)

                grade_var = tk.StringVar()
                grade_entry = tk.Entry(self.student_grades_frame, textvariable=grade_var)
                grade_entry.grid(row=i, column=1, padx=5, pady=5)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching students: {e}")

    def add_grades(self):
        section_id = self.section_var.get()
        if not section_id:
            messagebox.showerror("Error", "Please select a section.")
            return

        try:
            for student in self.students:
                student_id = student[2]
                grade = None  # Set grade to None initially
                for child in self.student_grades_frame.winfo_children():
                    if isinstance(child, tk.Entry):
                        if child.grid_info()["row"] == self.students.index(student):
                            grade = child.get()  # Get the grade entered by the instructor
                            break
                if grade is not None:
                    # Insert or update grade for the student
                    course_id= self.c.execute("SELECT course_id FROM section WHERE section_id = ?",(section_id,))
                    course_id = self.c.fetchone()[0]  # Fetch the course_id from the cursor
                    self.c.execute("INSERT OR REPLACE INTO grade (student_id, course_id, grade) VALUES (?, ?, ?)", (student_id, course_id, grade))
            self.conn.commit()
            messagebox.showinfo("Success", "Grades added successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding grades: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    if len(sys.argv) >= 2:
        instructor_id = sys.argv[1]
        print(f"Username received: {instructor_id}")
    else:
        messagebox.showerror("Error", "Instructor ID not provided.")
        instructor_id = 'kumar1v'
    app = InstructorGradeApp(root, instructor_id)
    root.mainloop()
