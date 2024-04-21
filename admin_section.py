import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import sys
import subprocess

class AddSectionWindow:
    def __init__(self, parent, refresh_callback):
        self.parent = parent
        self.refresh_callback = refresh_callback
        self.window = tk.Toplevel(parent)
        self.window.title("Add Section")
        self.window.geometry("300x300")
        self.window.configure(bg="#00415a")

        self.course_label = tk.Label(self.window, text="Select Course:", bg="#00415a",fg="white")
        self.course_label.place(relx=0.05, rely=0.07)
        self.course_var = tk.StringVar()
        self.course_combobox = ttk.Combobox(self.window, textvariable=self.course_var, state="readonly")
        self.course_combobox.place(relx=0.5, rely=0.07)

        self.instructor_label = tk.Label(self.window, text="Select Instructor:", bg="#00415a",fg="white")
        self.instructor_label.place(relx=0.05, rely=0.2)
        self.instructor_var = tk.StringVar()
        self.instructor_combobox = ttk.Combobox(self.window, textvariable=self.instructor_var, state="readonly")
        self.instructor_combobox.place(relx=0.5, rely=0.2)

        self.start_time_label = tk.Label(self.window, text="Start Time:", bg="#00415a",fg="white")
        self.start_time_label.place(relx=0.05, rely=0.33)
        self.start_time_var = tk.StringVar()
        self.start_time_combobox = ttk.Combobox(self.window, textvariable=self.start_time_var, state="readonly")
        self.start_time_combobox.place(relx=0.5, rely=0.33)

        self.end_time_label = tk.Label(self.window, text="End Time:", bg="#00415a",fg="white")
        self.end_time_label.place(relx=0.05, rely=0.47)
        self.end_time_var = tk.StringVar()
        self.end_time_combobox = ttk.Combobox(self.window, textvariable=self.end_time_var, state="readonly")
        self.end_time_combobox.place(relx=0.5, rely=0.47)

        self.day_label = tk.Label(self.window, text="Select Day:", bg="#00415a",fg="white")
        self.day_label.place(relx=0.05, rely=0.6)
        self.day_var = tk.StringVar()
        self.day_combobox = ttk.Combobox(self.window, textvariable=self.day_var, state="readonly")
        self.day_combobox.place(relx=0.5, rely=0.6)

        self.room_label = tk.Label(self.window, text="Room Number:", bg="#00415a",fg="white")
        self.room_label.place(relx=0.05, rely=0.73)
        self.room_entry = tk.Entry(self.window)
        self.room_entry.place(relx=0.5, rely=0.73)

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit_section,bg='#87CEEB')
        self.submit_button.place(relx=0.5, rely=0.87)

        # Populate course, instructor, and day dropdowns
        self.populate_course_dropdown()
        self.populate_instructor_dropdown()
        self.populate_day_dropdown()
        self.populate_time_dropdowns()

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

    def populate_day_dropdown(self):
        # Days of the week (Monday to Friday)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.day_combobox["values"] = days

    def populate_instructor_dropdown(self):
        try:
            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            instructors = c.execute("SELECT first_name, last_name FROM users WHERE role=?", ("Instructor",)).fetchall()
            self.instructor_combobox["values"] = [f"{instructor[0]} {instructor[1]}" for instructor in instructors]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching instructors: {e}")
        finally:
            if conn:
                conn.close()

    def populate_time_dropdowns(self):
        # Generate time options
        times = []
        for hour in range(7, 23):  # Hours from 07:00 AM to 10:00 PM
            for minute in range(0, 60, 30):  # Minutes with 30-minute interval
                time = f"{hour:02d}:{minute:02d} {'AM' if hour < 12 else 'PM'}"
                times.append(time)

        # Populate start time and end time dropdowns
        self.start_time_combobox["values"] = times
        self.end_time_combobox["values"] = times

    def submit_section(self):
        course_name = self.course_var.get()
        instructor_name = self.instructor_var.get()
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        room_number = self.room_entry.get()
        day = self.day_var.get()
        start_time = start_time + ' ('+day+ ')'
        end_time = end_time +' ('+ day+ ')'
        
        if not course_name or not instructor_name or not start_time or not end_time or not room_number:
            messagebox.showerror("Error", "Please fill in all fields.")

            return

        if start_time >= end_time:
            messagebox.showerror("Error", "time error.")
            return    
        try:
            conn = sqlite3.connect('user.db')
            c = conn.cursor()

            # Get course ID
            course_id = c.execute("SELECT course_id FROM course WHERE course_name=?", (course_name,)).fetchone()[0]
            # Get the maximum section ID
            max_section_id = c.execute("SELECT MAX(section_id) FROM section").fetchone()[0]

            # Increment the section ID
            if max_section_id is None:
                new_section_id = 'S1000'  # Start with 's1000' if there are no existing section IDs
            else:
                last_id = int(max_section_id[1:])  # Extract the numeric part of the last section ID
                new_section_id = 'S' + str(last_id + 1)  # Increment and format the new section ID
            
            # Get instructor ID
            instructor_fullname = instructor_name.split()
            instructor_id = c.execute("SELECT user_id FROM users WHERE first_name=? AND last_name=? AND role=?", (instructor_fullname[0], instructor_fullname[1], "Instructor")).fetchone()[0]

            # Insert new section into the database
            c.execute("INSERT INTO section (section_id,course_id, instructor_id, start_time, end_time, class_room) VALUES (?,?, ?, ?, ?, ?)",
                      (new_section_id,course_id, instructor_id, start_time, end_time, room_number))
            conn.commit()

            messagebox.showinfo("Success", "Section added successfully.")
            self.refresh_callback()
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
        self.root.geometry("900x600")
        self.root.configure(bg="#00415a") 
        
        # Connect to SQLite3 database
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()

        self.create_widgets()
        self.load_sections()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use the "clam" theme

        # Configure style for Treeview widget
        self.style.configure("Treeview",
                             background="#00415a",  # Background color
                             foreground="black",  # Font colo
                             fieldbackground="#00415a",
                             font=("Helvetica", 12))  # Field background color

        # Configure style for Treeview headings
        self.style.configure("Treeview.Heading",
                             background="#00415a",  # Heading background color
                             foreground="white",  # Heading font color
                             font=("Helvetica", 12, "bold"))  # Heading font

        self.section_table = ttk.Treeview(self.root, columns=("Section ID", "Course ID", "Instructor", "Start Time", "End Time", "Class Room"), show="headings")
        self.section_table.heading("Section ID", text="Section ID")
        self.section_table.heading("Course ID", text="Course ID")
        self.section_table.heading("Instructor", text="Instructor")
        self.section_table.heading("Start Time", text="Start Time")
        self.section_table.heading("End Time", text="End Time")
        self.section_table.heading("Class Room", text="Class Room")
        self.section_table.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.85)

        # Set column widths
        self.section_table.column("Section ID", width=120)
        self.section_table.column("Course ID", width=120)
        self.section_table.column("Instructor", width=200)
        self.section_table.column("Start Time", width=200)
        self.section_table.column("End Time", width=200)
        self.section_table.column("Class Room", width=120)

        self.add_button = tk.Button(self.root, text="Add Section", command=self.open_add_section_window,bg='#87CEEB')
        self.add_button.place(relx=0.01, rely=0.9, relwidth=0.1, relheight=0.05)

        self.delete_button = tk.Button(self.root, text="Delete Section(s)", command=self.delete_selected_sections,bg='#87CEEB')
        self.delete_button.place(relx=0.12, rely=0.9, relwidth=0.1, relheight=0.05)

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout,bg='#87CEEB')
        self.logout_button.place(relx=0.78, rely=0.9, relwidth=0.1, relheight=0.05)

        self.back_button = tk.Button(self.root, text="Back", command=self.back,bg='#87CEEB')
        self.back_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)

    def load_sections(self):
        # Clear previous section entries
        self.section_table.delete(*self.section_table.get_children())
        tag = "even"
        # Fetch sections from the database
        sections = self.c.execute("SELECT section_id, course_id, users.first_name || ' ' || users.last_name, start_time, end_time, class_room FROM section JOIN users ON section.instructor_id = users.user_id ORDER BY section.section_id").fetchall()
        for section in sections:
            self.section_table.insert("", "end", values=section, tags=(tag,))
            tag = "odd" if tag == "even" else "even"
        self.section_table.tag_configure("even", background="#f2f2f2")
        self.section_table.tag_configure("odd", background="#ffffff")

    def open_add_section_window(self):
        AddSectionWindow(self.root, self.load_sections)

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
        
    def logout(self):
        self.root.destroy()  # Close the current window
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\login_register.py', username], check=True)

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
    app = SectionManagementApp(root)
    root.mainloop()
