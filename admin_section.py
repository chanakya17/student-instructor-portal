import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
class AddSectionWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Add Section")

        self.course_label = tk.Label(self.window, text="Select Course:")
        self.course_label.grid(row=0, column=0, padx=5, pady=5)
        self.course_var = tk.StringVar()
        self.course_combobox = ttk.Combobox(self.window, textvariable=self.course_var, state="readonly")
        self.course_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.instructor_label = tk.Label(self.window, text="Select Instructor:")
        self.instructor_label.grid(row=1, column=0, padx=5, pady=5)
        self.instructor_var = tk.StringVar()
        self.instructor_combobox = ttk.Combobox(self.window, textvariable=self.instructor_var, state="readonly")
        self.instructor_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.start_time_label = tk.Label(self.window, text="Start Time:")
        self.start_time_label.grid(row=2, column=0, padx=5, pady=5)
        self.start_time_entry = tk.Entry(self.window)
        self.start_time_entry.grid(row=2, column=1, padx=5, pady=5)

        self.end_time_label = tk.Label(self.window, text="End Time:")
        self.end_time_label.grid(row=3, column=0, padx=5, pady=5)
        self.end_time_entry = tk.Entry(self.window)
        self.end_time_entry.grid(row=3, column=1, padx=5, pady=5)

        self.room_label = tk.Label(self.window, text="Room Number:")
        self.room_label.grid(row=4, column=0, padx=5, pady=5)
        self.room_entry = tk.Entry(self.window)
        self.room_entry.grid(row=4, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit_section)
        self.submit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Populate course and instructor dropdowns
        self.populate_course_dropdown()
        self.populate_instructor_dropdown()

    def populate_course_dropdown(self):
        try:
            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            courses = c.execute("SELECT course_name FROM course").fetchall()
            self.course_combobox["values"] = [course[0] for course in courses]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching courses: {e}")
        finally:
            if conn:
                conn.close()

    def populate_instructor_dropdown(self):
        try:
            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            instructors = c.execute("SELECT first_name, last_name FROM users WHERE role=?", ("Instructor",)).fetchall()
            print(instructors)
            self.instructor_combobox["values"] = [f"{instructor[0]} {instructor[1]}" for instructor in instructors]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching instructors: {e}")
        finally:
            if conn:
                conn.close()

    def submit_section(self):
        course_name = self.course_var.get()
        instructor_name = self.instructor_var.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        room_number = self.room_entry.get()

        if not course_name or not instructor_name or not start_time or not end_time or not room_number:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            conn = sqlite3.connect('user.db')
            c = conn.cursor()

            # Get course ID
            course_id = c.execute("SELECT course_id FROM course WHERE course_name=?", (course_name,)).fetchone()[0]
            # Get the maximum section ID
            max_section_id = c.execute("SELECT MAX(section_id) FROM section").fetchone()[0]
            if max_section_id is None:
                max_section_id = 0

            # Increment the course ID
            new_section_id = max_section_id + 1

            # Get instructor ID
            instructor_fullname = instructor_name.split()
            print(instructor_fullname)
            instructor_id = c.execute("SELECT user_id FROM users WHERE first_name=? AND last_name=? AND role=?", (instructor_fullname[0], instructor_fullname[1], "Instructor")).fetchone()[0]
            print(instructor_id)
            # Insert new section into the database
            c.execute("INSERT INTO section (section_id,course_id, instructor_id, start_time, end_time, class_room) VALUES (?,?, ?, ?, ?, ?)",
                      (new_section_id,course_id, instructor_id, start_time, end_time, room_number))
            conn.commit()

            messagebox.showinfo("Success", "Section added successfully.")
            self.window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding section: {e}")
        finally:
            if conn:
                conn.close()
                
class SectionManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Section Management")
        
        # Connect to SQLite3 database
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()

        self.create_widgets()
        self.load_sections()

    def create_widgets(self):
        self.section_table = ttk.Treeview(self.root, columns=("Section ID", "Course ID", "Instructor ID", "Start Time", "End Time", "Class Room"), show="headings")
        self.section_table.heading("Section ID", text="Section ID")
        self.section_table.heading("Course ID", text="Course ID")
        self.section_table.heading("Instructor ID", text="Instructor ID")
        self.section_table.heading("Start Time", text="Start Time")
        self.section_table.heading("End Time", text="End Time")
        self.section_table.heading("Class Room", text="Class Room")
        self.section_table.pack(padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Section", command=self.open_add_section_window)
        self.add_button.pack(side="left", padx=5, pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Selected Section(s)", command=self.delete_selected_sections)
        self.delete_button.pack(side="left", padx=5, pady=5)

    def load_sections(self):
        # Clear previous section entries
        self.section_table.delete(*self.section_table.get_children())

        # Fetch sections from the database
        sections = self.c.execute("SELECT * FROM section").fetchall()
        for section in sections:
            self.section_table.insert("", "end", values=section)

    def open_add_section_window(self):
        AddSectionWindow(self.root)
        self.load_sections()

    def delete_selected_sections(self):
        selected_items = self.section_table.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select section(s) to delete.")
            return

        for selected_item in selected_items:
            # Get the section ID of the selected item
            section_id = self.section_table.item(selected_item, "values")[0]

            try:
                # Delete the section from the database
                self.c.execute("DELETE FROM section WHERE section_id=?", (section_id,))
                self.conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error deleting section {section_id}: {e}")

        # Refresh the section list
        self.load_sections()
        messagebox.showinfo("Success", "Selected section(s) deleted successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SectionManagementApp(root)
    root.mainloop()