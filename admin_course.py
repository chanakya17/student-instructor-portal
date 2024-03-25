import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class AddCourseWindow:
    def __init__(self, parent, refresh_callback):
        self.parent = parent
        self.refresh_callback = refresh_callback
        self.window = tk.Toplevel(parent)
        self.window.title("Add Course")

        self.course_name_label = tk.Label(self.window, text="Course Name:")
        self.course_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.course_name_entry = tk.Entry(self.window)
        self.course_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.class_label = tk.Label(self.window, text="Class:")
        self.class_label.grid(row=1, column=0, padx=5, pady=5)
        self.class_var = tk.StringVar()
        self.class_combobox = ttk.Combobox(self.window, textvariable=self.class_var, values=["9", "10", "11", "12"])
        self.class_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.credits_label = tk.Label(self.window, text="Credits:")
        self.credits_label.grid(row=2, column=0, padx=5, pady=5)
        self.credits_entry = tk.Entry(self.window)
        self.credits_entry.grid(row=2, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit_course)
        self.submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def submit_course(self):
        course_name = self.course_name_entry.get()
        class_ = self.class_var.get()
        credits = self.credits_entry.get()

        if not course_name or not class_ or not credits:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            # Connect to SQLite3 database
            conn = sqlite3.connect('user.db')
            c = conn.cursor()

            # Get the maximum course ID
            max_course_id = c.execute("SELECT MAX(course_id) FROM course").fetchone()[0]
            if max_course_id is None:
                max_course_id = 0

            # Increment the course ID
            new_course_id = max_course_id + 1

            # Insert the new course into the database
            c.execute("INSERT INTO course (course_id, course_name, class, credits) VALUES (?, ?, ?, ?)", (new_course_id, course_name, class_, credits))
            conn.commit()

            messagebox.showinfo("Success", "Course added successfully.")
            self.refresh_callback()
            self.window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding course: {e}")
        finally:
            if conn:
                conn.close()

class AdminCourseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Course Management")
        
        # Connect to SQLite3 database
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()

        self.create_widgets()
        self.load_courses()

    def create_widgets(self):
        self.course_table = ttk.Treeview(self.root, columns=("Course ID", "Name", "Class", "Credits"), show="headings")
        self.course_table.heading("Course ID", text="Course ID")
        self.course_table.heading("Name", text="Name")
        self.course_table.heading("Class", text="Class")
        self.course_table.heading("Credits", text="Credits")
        self.course_table.pack(padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Selected Course(s)", command=self.delete_selected_courses)
        self.delete_button.pack(pady=5)

        self.add_button = tk.Button(self.root, text="Add Course", command=self.open_add_course_window)
        self.add_button.pack(pady=5)

    def load_courses(self):
        # Clear previous course entries
        self.course_table.delete(*self.course_table.get_children())

        # Fetch courses from the database
        courses = self.c.execute("SELECT * FROM course").fetchall()
        for course in courses:
            self.course_table.insert("", "end", values=course)

    def delete_selected_courses(self):
        selected_items = self.course_table.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select course(s) to delete.")
            return

        try:
            # Connect to SQLite3 database
            conn = sqlite3.connect('user.db')
            c = conn.cursor()

            for item in selected_items:
                # Get the course ID of the selected item
                course_id = self.course_table.item(item, "values")[0]

                # Delete the course from the database
                c.execute("DELETE FROM course WHERE course_id=?", (course_id,))
            
            conn.commit()

            messagebox.showinfo("Success", "Selected course(s) deleted successfully.")
            self.load_courses()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting course(s): {e}")
        finally:
            if conn:
                conn.close()

    def open_add_course_window(self):
        AddCourseWindow(self.root, self.load_courses)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminCourseApp(root)
    root.mainloop()
