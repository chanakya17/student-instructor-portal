import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys

class StudentGradeApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Student Grade Checker")

        # Connect to SQLite3 database
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()

        self.username = username

        self.create_widgets()

    def create_widgets(self):
        self.course_label = tk.Label(self.root, text="Select Course:")
        self.course_label.grid(row=0, column=0, padx=5, pady=5)
        self.course_var = tk.StringVar()
        self.course_combobox = ttk.Combobox(self.root, textvariable=self.course_var, state="readonly", width=30)
        self.course_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.display_grades)
        self.submit_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.grades_text = tk.Text(self.root, width=40, height=10)
        self.grades_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Populate course dropdown
        self.populate_course_dropdown()

    def populate_course_dropdown(self):
        try:
            student_id = self.username
            courses = self.c.execute('''SELECT course_name 
                    FROM course 
                    JOIN section ON course.course_id = section.course_id 
                    JOIN course_reg ON section.section_id = course_reg.section_id 
                    WHERE course_reg.student_id=? AND course_reg.status = 'y' ''', (student_id,)).fetchall()
            self.course_combobox["values"] = [course[0] for course in courses]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching courses: {e}")

    def display_grades(self):
        course_name = self.course_var.get()

        if not course_name:
            messagebox.showerror("Error", "Please select a course.")
            return

        try:
            student_id = self.username
            course_id = self.c.execute("SELECT course_id FROM course WHERE course_name=?", (course_name,)).fetchone()[0]

            grades = self.c.execute("SELECT grade FROM grade WHERE student_id=? AND course_id=?", (student_id, course_id)).fetchall()

            self.grades_text.delete("1.0", tk.END)
            if grades:
                self.grades_text.insert(tk.END, "Grades for {} in {}:\n".format(self.username, course_name))
                for grade in grades:
                    self.grades_text.insert(tk.END, "{}\n".format(grade[0]))
            else:
                self.grades_text.insert(tk.END, "No grades found for {} in {}.".format(self.username, course_name))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching grades: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    if len(sys.argv) >= 2:
        username = sys.argv[1]
        print(f"Username received: {username}")
    else:
        messagebox.showerror("Error", "Username not provided.")
        username= 'ander1e'
    app = StudentGradeApp(root, username)
    root.mainloop()
