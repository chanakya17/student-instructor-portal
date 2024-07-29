import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys
import subprocess

class StudentGradeApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Student Grade Checker")
        self.root.geometry("800x600")
        self.root.configure(bg="#00415a")
        # Connect to SQLite3 database
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()

        self.username = username
#chanakya
        self.create_widgets()

    def create_widgets(self):
        self.root.style = ttk.Style()
        self.root.style.theme_use("clam")  # Use the "clam" theme

        # Configure style for Treeview widget
        self.root.style.configure("NoBorder.Treeview",
                             background="#00415a",  # Background color
                             foreground="black",  # Font color
                             fieldbackground="#00415a",
                             font=("Helvetica", 12))
        self.root.style.configure("NoBorder.Treeview.Heading",
                             background="#00415a",  # Heading background color
                             foreground="white",  # Heading font color
                             font=("Helvetica", 12, "bold"))
        
        self.tree = ttk.Treeview(self.root, columns=('Course', 'Instructor', 'Credits', 'Grade'), show="headings", height=24, style="NoBorder.Treeview")
        self.tree.heading('Course', text='Course')
        self.tree.heading('Instructor', text='Instructor')
        self.tree.heading('Credits', text='Credits')
        self.tree.heading('Grade', text='Grade')

        self.tree.column('Course', width=150)
        self.tree.column('Instructor', width=110)
        self.tree.column('Credits', width=110)
        self.tree.column('Grade', width=110)

        self.tree.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.85)

        self.back_button = tk.Button(self.root, text="Back", command=self.back, bg='#87CEEB')
        self.back_button.place(relx=0.78, rely=0.9, relwidth=0.1, relheight=0.05)

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout, bg='#87CEEB')
        self.logout_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)
        
        self.grade_details = tk.Button(self.root, text="View Grade Details", command=self.view_grade_details, bg='#87CEEB')
        self.grade_details.place(relx=0.03, rely=0.9, relwidth=0.1, relheight=0.05)

        # Populate course treeview
        self.populate_course_treeview()

    def populate_course_treeview(self):
        try:
            student_id = self.username
            courses = self.c.execute('''SELECT course.course_name, users.first_name || ' ' || users.last_name, course.credits, grade.grade 
                    FROM course 
                    JOIN section ON course.course_id = section.course_id 
                    JOIN users ON section.instructor_id = users.user_id 
                    LEFT JOIN grade ON section.section_id = grade.section_id AND grade.student_id = ?
                    JOIN course_reg ON section.section_id = course_reg.section_id 
                    WHERE course_reg.student_id=? AND course_reg.status = 'y' ''', (student_id, student_id)).fetchall()
            tag = "even"
            for course in courses:
                self.tree.insert('', 'end', values=(course[0], course[1], course[2], course[3] if course[3] else 'N/A'), tags=(tag,))
                tag = "odd" if tag == "even" else "even"
            self.tree.tag_configure("even", background="#f2f2f2")
            self.tree.tag_configure("odd", background="#ffffff")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching courses: {e}")

    def logout(self):
        self.root.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\login_register.py'])

    def back(self):
        self.root.destroy()
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\student_dashboard.py', self.username], check=True)

    def view_grade_details(self):
        popup = tk.Toplevel(self.root)
        popup.title("Grade Details")
        # popup.geometry("400x300")
        popup.configure(bg="#00415a")
        grade_data = {
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
        grade_details_label = tk.Label(popup, text="Grade Details", font=('Arial', 14, 'bold'), foreground="white", background="#00415a")
        grade_details_label.grid(row=0,column=1,sticky=tk.W)
        tk.Label(popup, text="Grade", font=('Arial', 10, 'bold'), foreground="white", background="#00415a").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(popup, text="GPA", font=('Arial', 10, 'bold'), foreground="white", background="#00415a").grid(row=1, column=1, padx=10, pady=5)
        tk.Label(popup, text="Percentage Range", font=('Arial', 10, 'bold'), foreground="white", background="#00415a").grid(row=1, column=2, padx=10, pady=5)
        grade_labels = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'E']
        for i, grade in enumerate(grade_labels):
            grade_label = tk.Label(popup, text=grade, font=('Arial', 10), foreground="white", background="#00415a")
            grade_label.grid(row=i+2, column=0, padx=20, pady=5)

            # Add corresponding GPA
            gpa_label = tk.Label(popup, text=grade_data[grade]["gpa"], font=('Arial', 10), foreground="white", background="#00415a")
            gpa_label.grid(row=i+2, column=1, padx=20, pady=5)

            # Add corresponding percentage range
            percentage_label = tk.Label(popup, text=grade_data[grade]["percentage_range"], font=('Arial', 10), foreground="white", background="#00415a")
            percentage_label.grid(row=i+2, column=2, padx=20, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    if len(sys.argv) >= 2:
        username = sys.argv[1]
        print(f"Username received in grade_student: {username}")
    else:
        username= 'musuk2s'
    app = StudentGradeApp(root, username)
    root.mainloop()
