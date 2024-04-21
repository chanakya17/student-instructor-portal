import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
import sqlite3
import subprocess

class AddCourseWindow:
    def __init__(self, parent, refresh_callback):
        self.parent = parent
        self.refresh_callback = refresh_callback
        self.window = tk.Toplevel(parent)
        self.window.title("Add Course")
        self.window.geometry("300x200")
        self.window.configure(bg="#00415a")  # Set background color

        self.course_name_label = tk.Label(self.window, text="Course Name:", bg="#00415a",fg="white")
        self.course_name_label.place(relx=0.1, rely=0.1)
        self.course_name_entry = tk.Entry(self.window)
        self.course_name_entry.place(relx=0.5, rely=0.1)

        self.class_label = tk.Label(self.window, text="Class:", bg="#00415a",fg="white")
        self.class_label.place(relx=0.1, rely=0.3)
        self.class_var = tk.StringVar()
        self.class_combobox = ttk.Combobox(self.window, textvariable=self.class_var, values=["9", "10", "11", "12"])
        self.class_combobox.place(relx=0.5, rely=0.3)

        self.credits_label = tk.Label(self.window, text="Credits:", bg="#00415a",fg="white")
        self.credits_label.place(relx=0.1, rely=0.5)
        self.credits_var = tk.StringVar()
        self.credits_combobox = ttk.Combobox(self.window, textvariable=self.credits_var, values=["1", "2", "3", "4"])
        self.credits_combobox.place(relx=0.5, rely=0.5)

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit_course, bg='#87CEEB')
        self.submit_button.place(relx=0.5, rely=0.7)

    def submit_course(self):
        course_name = self.course_name_entry.get().title()
        class_ = self.class_var.get().title()
        credits = self.credits_combobox.get().title()

        if not course_name or not class_ or not credits:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            # Connect to SQLite3 database
            conn = sqlite3.connect('user.db')  
            c = conn.cursor()

            # Get the maximum course ID
            max_course_id = c.execute("SELECT MAX(course_id) FROM course").fetchone()[0]
            
            # Increment the course ID
            if max_course_id is None:
                new_course_id = 'C1000'  # Start with 'c1000' if there are no existing course IDs
            else:
                last_id = int(max_course_id[1:])  # Extract the numeric part of the last course ID
                new_course_id = 'C' + str(last_id + 1).zfill(4)  # Increment and format the new course ID
        
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
        self.root.geometry("900x600")
        self.root.configure(bg="#00415a")  # Set background color
        
        # Connect to SQLite3 database
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()

        self.create_widgets()
        self.load_courses()

    def create_widgets(self):
        # Set the desired width and height for the Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#00415a", fieldbackground="#00415a", font=("Arial", 12))
        # Configure style for Treeview headings
        self.style.configure("Treeview.Heading",
                             background="#00415a",  # Heading background color
                             foreground="white",  # Heading font color
                             font=("Helvetica", 12, "bold"))  # Heading font

        self.course_table = ttk.Treeview(self.root, columns=("Course ID", "Name", "Class", "Credits"), show="headings")
        self.course_table.heading("Course ID", text="Course ID")
        self.course_table.heading("Name", text="Name")
        self.course_table.heading("Class", text="Class")
        self.course_table.heading("Credits", text="Credits")
        self.course_table.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.85)

        # Set column widths
        self.course_table.column("Course ID", width=150)
        self.course_table.column("Name", width=320)
        self.course_table.column("Class", width=200)
        self.course_table.column("Credits", width=200)


        self.add_button = tk.Button(self.root, text="Add Course", command=self.open_add_course_window, bg='#87CEEB')
        self.add_button.place(relx=0.01, rely=0.9, relwidth=0.1, relheight=0.05)

        self.delete_button = tk.Button(self.root, text="Delete Course(s)", command=self.delete_selected_courses, bg='#87CEEB')
        self.delete_button.place(relx=0.12, rely=0.9, relwidth=0.1, relheight=0.05)

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout, bg='#87CEEB')
        self.logout_button.place(relx=0.78, rely=0.9, relwidth=0.1, relheight=0.05)

        self.back_button = tk.Button(self.root, text="Back", command=self.back, bg='#87CEEB')
        self.back_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)
        
    def load_courses(self):
        # Clear previous course entries
        self.course_table.delete(*self.course_table.get_children())
        tag = "even"
        # Fetch courses from the database
        courses = self.c.execute("SELECT * FROM course").fetchall()
        
        for course in courses:
            self.course_table.insert("", "end", values=course, tags=(tag,))
            tag = "odd" if tag == "even" else "even"
        self.course_table.tag_configure("even", background="#f2f2f2")
        self.course_table.tag_configure("odd", background="#ffffff")

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
        
    def logout(self):
        self.root.destroy()  # Close the current window
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\login_register.py'])

    def back(self):
        self.root.destroy()  # Close the current window
        subprocess.run(['python', 'E:\\cmu\\BIS 698\\misc code\\admin_dashboard.py', username], check=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    if len(sys.argv) >= 2:
        username = sys.argv[1]
        print(f"Username received in admin_dashboard.py: {username}")
    else:
        username = 'mechi1c'
    app = AdminCourseApp(root)
    root.mainloop()
