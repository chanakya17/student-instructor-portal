import tkinter as tk
from tkinter import ttk
import sys
from database import User
import subprocess

class StudentDashboard(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title("Student Dashboard")

        self.user = User()
        self.username = username
        self.firstname = self.user.get_details('first_name', username)
        self.lastname = self.user.get_details('last_name', username)
        self.role = self.user.get_details('role', username)
        self.cls = self.user.get_details('class', username)

        # Load an image (replace 'your_image_path.jpg' with the actual path to your image)
        self.image_path = "E:/cmu/BIS 698/misc code/OIG2.png"
        self.image = tk.PhotoImage(file=self.image_path)

        self.create_widgets()

    def create_widgets(self):
        # Create a label to display the image
        image_label = tk.Label(self, image=self.image)
        image_label.pack()

        # Frame for student details
        details_frame = ttk.Frame(self)
        details_frame.pack(pady=10)

        # Labels and entry widgets for student details
        ttk.Label(details_frame, text="First Name: ").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        sd_first_name_label = ttk.Label(details_frame, text=self.firstname)
        sd_first_name_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(details_frame, text="Last Name: ").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        sd_last_name_label = ttk.Label(details_frame, text=self.lastname)
        sd_last_name_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # ttk.Label(details_frame, text="Class: ").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        # sd_class_label = ttk.Label(details_frame, text=self.cls)
        # sd_class_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(details_frame, text="Username: ").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        sd_username_label = ttk.Label(details_frame, text=self.username)
        sd_username_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Frame for buttons
        button_frame = ttk.Frame(self)
        button_frame.pack()

        # Buttons
        course_reg_button = ttk.Button(button_frame, text="Course Registration", command=self.course_reg_button_click)
        course_reg_button.grid(row=0, column=0, padx=5, pady=5)

        attendence_button = ttk.Button(button_frame, text="Attendance", command=self.attendence_button_click)
        attendence_button.grid(row=0, column=1, padx=5, pady=5)

        grades_button = ttk.Button(button_frame, text="Grades", command=self.grades_button_click)
        grades_button.grid(row=0, column=2, padx=5, pady=5)

        notifications_button = ttk.Button(button_frame, text="Notifications", command=self.notifications_button_click)
        notifications_button.grid(row=0, column=3, padx=5, pady=5)

        logout_button = ttk.Button(button_frame, text="Logout", command=self.logout_button_click)
        logout_button.grid(row=1, column=2, padx=5, pady=5)

    def course_reg_button_click(self):
        # Add functionality for button 1
        print("Button 1 clicked")

    def attendence_button_click(self):
        # Add functionality for button 2
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\attendence_try.py', username], check=True)
        print("Button 2 clicked")

    def grades_button_click(self):
        # Add functionality for button 3
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\instructor_grade.py', username], check=True)
        print("Button 3 clicked")

    def notifications_button_click(self):
        # Add functionality for button 4
        print("Button 4 clicked")
    
    def logout_button_click(self):
        #add functionality for button 4
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\login_register.py', username], check=True)
        print("Logout button clicked")


# Retrieve the username from command-line arguments
if len(sys.argv) >= 2:
    username = sys.argv[1]
    print(f"Username received in student_dashboard.py: {username}")
else:
    username = 'mechi1c'

# Create an instance of the StudentDashboard class
app = StudentDashboard(username)

# Run the Tkinter main loop
app.mainloop()
