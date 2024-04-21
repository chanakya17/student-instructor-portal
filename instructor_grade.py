import tkinter as tk
from tkinter import ttk, messagebox
import sys
import sqlite3
import subprocess

class InstructorGradeApp:
    def __init__(self, root, instructor_id):
        self.root = root
        self.root.title("Instructor Grade Management")
        self.root.geometry("800x600")
        self.root.configure(bg="#00415a")
        # Connect to SQLite3 database
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()
        self.grade_data = {
            "A": {"gpa": 4.0, "percentage_range": "(90-100)"},
            "A-": {"gpa": 3.7, "percentage_range": "(85-89)"},
            "B+": {"gpa": 3.3, "percentage_range": "(80-84)"},
            "B": {"gpa": 3.0, "percentage_range": "(75-79)"},
            "B-": {"gpa": 2.7, "percentage_range": "(70-74)"},
            "C+": {"gpa": 2.3, "percentage_range": "(65-69)"},
            "C": {"gpa": 2.0, "percentage_range": "(60-64)"},
            "C-": {"gpa": 1.7, "percentage_range": "(55-59)"},
            "D+": {"gpa": 1.3, "percentage_range": "(50-54)"},
            "D": {"gpa": 1.0, "percentage_range": "(45-49)"},
            "D-": {"gpa": 0.7, "percentage_range": "(40-44)"},
            "E": {"gpa": 0.0, "percentage_range": "(Below 40)"}
        }
        self.instructor_id = instructor_id

        self.create_widgets()

    def create_widgets(self):
        self.section_label = tk.Label(self.root, text="Select Section:", font=('Arial', 10, 'bold'), foreground="white", background="#00415a")
        self.section_label.place(relx=0.01, rely=0.02)
        self.section_var = tk.StringVar()
        self.section_combobox = ttk.Combobox(self.root, textvariable=self.section_var, state="readonly")
        self.section_combobox.place(relx=0.15, rely=0.02)

        self.course_name_label = tk.Label(self.root, text="Course: ", font=('Arial', 10, 'bold'),foreground="white", background="#00415a")
        self.course_name_label.place(relx=0.5, rely=0.02,relheight=0.5)

        # Create a canvas to hold the student grades frame with scrolling capability
        self.canvas = tk.Canvas(self.root, bg="#00415a", bd=0, highlightthickness=0)
        self.canvas.place(relx=0.2, rely=0.1, relwidth=0.68, relheight=0.7)  # Adjust relheight as needed

        # Add a scrollbar for the canvas
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(relx=0.98, rely=0.1, relheight=0.75)

        # Create a frame within the canvas to hold the student grades
        self.student_grades_frame = tk.Frame(self.canvas, bg="#00415a", width=750, height=400)  # Adjust width and height as needed
        self.canvas.create_window((0, 0), window=self.student_grades_frame, anchor="nw")

        self.add_grades_button = tk.Button(self.root, text="Add Grades", command=self.add_grades, bg='#87CEEB', font=('Arial', 10, 'bold'))
        self.add_grades_button.place(relx=0.01, rely=0.9, relwidth=0.1, relheight=0.05)

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout, bg='#87CEEB', font=('Arial', 10, 'bold'))
        self.logout_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)

        self.back_button = tk.Button(self.root, text="Back", command=self.back, bg='#87CEEB', font=('Arial', 10, 'bold'))
        self.back_button.place(relx=0.78, rely=0.9, relwidth=0.1, relheight=0.05)

        #grade details
        self.grade_details_frame = tk.Frame(self.root, bg="#00415a")
        self.grade_details_frame.place(relx=0.6, rely=0.1, relwidth=0.25, relheight=0.75)
        tk.Label(self.grade_details_frame, text="Grade", font=('Arial', 10, 'bold'), foreground="white", background="#00415a").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.grade_details_frame, text="GPA", font=('Arial', 10, 'bold'), foreground="white", background="#00415a").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.grade_details_frame, text="Percentage Range", font=('Arial', 10, 'bold'), foreground="white", background="#00415a").grid(row=0, column=2, padx=10, pady=5)
        grade_labels = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'E']
        for i, grade in enumerate(grade_labels):
            grade_label = tk.Label(self.grade_details_frame, text=grade, font=('Arial', 10), foreground="white", background="#00415a")
            grade_label.grid(row=i+1, column=0, padx=20, pady=5)

            # Add corresponding GPA
            gpa_label = tk.Label(self.grade_details_frame, text=self.grade_data[grade]["gpa"], font=('Arial', 10), foreground="white", background="#00415a")
            gpa_label.grid(row=i+1, column=1, padx=20, pady=5)

            # Add corresponding percentage range
            percentage_label = tk.Label(self.grade_details_frame, text=self.grade_data[grade]["percentage_range"], font=('Arial', 10), foreground="white", background="#00415a")
            percentage_label.grid(row=i+1, column=2, padx=20, pady=5)
        # Populate section dropdown
        self.populate_section_dropdown()
        self.section_combobox.bind("<<ComboboxSelected>>", self.load_students)

        # Configure the canvas to scroll
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

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
            course_name = self.c.execute("SELECT course.course_name FROM section INNER JOIN course ON section.course_id = course.course_id WHERE section.section_id=?", (section_id,)).fetchone()[0]
            self.course_name_label.config(text="Course: "+course_name)
            print(course_name)

            self.students = self.c.execute("SELECT users.user_id, users.first_name, users.last_name FROM users INNER JOIN course_reg ON users.user_id = course_reg.student_id WHERE course_reg.section_id=? AND users.role= 'Student' AND course_reg.status='y'", (section_id,)).fetchall()

            # Clear any existing widgets in the student_grades_frame
            for widget in self.student_grades_frame.winfo_children():
                widget.destroy()

            # Dictionary to store existing grades
            self.existing_grades = {}

            # Add student names and grade entry fields
            for i, student in enumerate(self.students):
                student_name = f"{student[1]} {student[2]}"
                student_label = tk.Label(self.student_grades_frame, text=student_name, foreground="white", background="#00415a", font=('Arial', 10, 'bold'))
                student_label.grid(row=i, column=0, padx=5, pady=5)

                grade_var = tk.StringVar()
                grade = self.c.execute("SELECT grade FROM grade WHERE grade.section_id=? AND student_id=? AND course_id=(SELECT course_id FROM section WHERE section.section_id=?)", (section_id,student[0], section_id)).fetchone()
                if grade:
                    grade_var.set(grade[0])
                    self.existing_grades[student[0]] = grade[0]  # Store existing grade in the dictionary
                else:
                    self.existing_grades[student[0]] = None

                # Adding validation for grade entry
                validate_grade = self.root.register(self.validate_grade)
                grade_entry = tk.Entry(self.student_grades_frame, textvariable=grade_var, validate="key", validatecommand=(validate_grade, "%P"))
                grade_entry.grid(row=i, column=1, padx=5, pady=5)

            # Update the scroll region of the canvas
            self.canvas.update_idletasks()  # Ensure all widgets are properly configured
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching students: {e}")

    def add_grades(self):
        section_id = self.section_var.get()
        if not section_id:
            messagebox.showerror("Error", "Please select a section.")
            return

        try:
            for student in self.students:
                student_id = student[0]
                grade = None  # Set grade to None initially
                for child in self.student_grades_frame.winfo_children():
                    if isinstance(child, tk.Entry):
                        if child.grid_info()["row"] == self.students.index(student):
                            grade = child.get()  # Get the grade entered by the instructor
                            break
                existing_grade = self.existing_grades.get(student_id)
                if grade is not None:
                    if existing_grade is None:
                        # Insert grade for the student if it does not exist
                        if grade:
                            course_id = self.c.execute("SELECT course_id FROM section WHERE section_id = ?",(section_id,))
                            course_id = self.c.fetchone()[0]  # Fetch the course_id from the cursor
                            self.c.execute("INSERT INTO grade (student_id, course_id, section_id, grade) VALUES (?, ?, ?,?)", (student_id, course_id,section_id, grade))
                    elif grade != existing_grade:
                        # Update grade for the student if modified
                        course_id = self.c.execute("SELECT course_id FROM section WHERE section_id = ?",(section_id,))
                        course_id = self.c.fetchone()[0]  # Fetch the course_id from the cursor
                        self.c.execute("UPDATE grade SET grade=? WHERE student_id=? AND course_id=? AND section_id=?", (grade, student_id, course_id,section_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Grades added successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding grades: {e}")

    def logout(self):
        self.root.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\login_register.py'])

    def back(self):
        self.root.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\instructor_dashboard.py', self.instructor_id], check=True)

    def validate_grade(self, new_value):
        # Validation function for grade entry
        valid_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'E']
        if new_value in valid_grades or new_value == "":
            return True
        else:
            messagebox.showerror("Error", "Invalid grade. Please enter one of: A, A-, B+, B, B-, C+, C, C-, D+, D, D-, E")
            return False

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.state('zoomed')
    root.configure(bg="#00415a")
    # Retrieving the username from command-line arguments
    if len(sys.argv) >= 2:
        instructor_id = sys.argv[1]
        print(f"Username received in inst_grade: {instructor_id}")
    else:
        instructor_id = 'kumar1v'
    app = InstructorGradeApp(root, instructor_id)
    root.mainloop()
