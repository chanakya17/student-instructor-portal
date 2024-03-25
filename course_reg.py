import tkinter as tk
from tkinter import messagebox
import sqlite3

class CourseRegistrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Course Registration")
        
        self.conn = sqlite3.connect('course_registration.db')
        self.c = self.conn.cursor()
        self.create_table()

        self.action_var = tk.StringVar(value="Register")
        
        self.create_widgets()
        self.refresh_course_list()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS courses
                          (id INTEGER PRIMARY KEY, section_id INTEGER, course_name TEXT, instructor_name TEXT, room_no TEXT, timings TEXT, status TEXT)''')
        self.conn.commit()

    def create_widgets(self):
        self.course_frame = tk.Frame(self)
        self.course_frame.pack(padx=20, pady=20)
        
        tk.Label(self.course_frame, text="Select Action:").grid(row=0, column=0, sticky="w")
        self.register_radio = tk.Radiobutton(self.course_frame, text="Register", variable=self.action_var, value="Register")
        self.drop_radio = tk.Radiobutton(self.course_frame, text="Drop", variable=self.action_var, value="Drop")
        self.register_radio.grid(row=0, column=1)
        self.drop_radio.grid(row=0, column=2)

        self.refresh_button = tk.Button(self.course_frame, text="Refresh Courses", command=self.refresh_course_list)
        self.refresh_button.grid(row=0, column=3)

    def refresh_course_list(self):
        self.clear_course_buttons()
        
        courses = self.c.execute("SELECT * FROM courses").fetchall()
        print(courses)  # Print out fetched courses for debugging
        for index, course in enumerate(courses):
            section_id, course_name, instructor_name, room_no, timings, status = course
            
            course_info_label = tk.Label(self.course_frame, text=f"Section ID: {section_id}, Course: {course_name}, Instructor: {instructor_name}, Room: {room_no}, Timings: {timings}")
            course_info_label.grid(row=index+1, column=0, columnspan=4, sticky="w")

            submit_button = tk.Button(self.course_frame, text="Submit", command=lambda course_info=course: self.select_course(course_info, "Register"))
            submit_button.grid(row=index+1, column=4, padx=5)
            
            drop_button = tk.Button(self.course_frame, text="Drop", command=lambda course_info=course: self.select_course(course_info, "Drop"))
            drop_button.grid(row=index+1, column=5, padx=5)

    def select_course(self, course_info, action):
        section_id, course_name, instructor_name, room_no, timings, status = course_info
        if action == "Register":
            response = messagebox.askyesno("Confirmation", f"Do you want to register for {course_name}?")
        elif action == "Drop":
            response = messagebox.askyesno("Confirmation", f"Do you want to drop {course_name}?")
        
        if response:
            self.handle_registration(section_id, action)
            self.refresh_course_list()

    def handle_registration(self, section_id, action):
        if action == "Register":
            self.c.execute("UPDATE courses SET status='Registered' WHERE section_id=?", (section_id,))
        elif action == "Drop":
            self.c.execute("UPDATE courses SET status=NULL WHERE section_id=?", (section_id,))
        self.conn.commit()

    def clear_course_buttons(self):
        for widget in self.course_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = CourseRegistrationApp()
    app.mainloop()
