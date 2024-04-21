import tkinter as tk
from tkinter import ttk
import sys
from database import User
import subprocess
from tkinter import font

class StudentDashboard(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title("Student Dashboard")
        self.state('zoomed')
        self.geometry("900x600")
        self.configure(bg="#00415a") 

        self.user = User()
        self.username = username
        self.firstname = self.user.get_details('first_name', username)
        self.lastname = self.user.get_details('last_name', username)
        self.role = self.user.get_details('role', username)
        self.cls = self.user.get_details('class', username)

        # Load an image (replace 'your_image_path.jpg' with the actual path to your image)
        # self.image_path = "E:/cmu/BIS 698/misc code/OIG2.png"
        # self.image = tk.PhotoImage(file=self.image_path)
        self.image_path = "E:/cmu/BIS 698/misc code/cmu high scl.png"
        self.image = tk.PhotoImage(file=self.image_path)

        self.create_widgets()

    def create_widgets(self):
        fg="white"
        bg="#00415a"
        custom_font = font.Font(family="Arial", size=24, weight="bold")
        # Create a label to display the image
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.place(relx=0.5, rely=0.0, anchor=tk.N)
        # self.welcome_label = tk.Label(self, text="Welcome ", 
        #                               foreground=fg,
        #                               background=bg,
        #                               font=custom_font)
        # self.welcome_label.place(relx=0.05, rely=0.4, anchor=tk.W)
        self.firstname_label = tk.Label(self, text=('Welcome'+' '+self.firstname +' '+ self.lastname), 
                                        foreground=fg,
                                        background=bg,
                                        font=custom_font)
        self.firstname_label.place(relx=0.05, rely=0.4, anchor=tk.W)

        
        # # Labels and entry widgets for student details
        # self.firstname_label = tk.Label(self, text="First Name: ", foreground=fg, background=bg)
        # self.firstname_label.place(relx=0.2, rely=0.6, anchor=tk.W)
        # self.firstname_value_label = tk.Label(self, text=self.firstname, foreground=fg, background=bg)
        # self.firstname_value_label.place(relx=0.4, rely=0.6, anchor=tk.W)

        # self.lastname_label = tk.Label(self, text="Last Name: ", foreground=fg, background=bg)
        # self.lastname_label.place(relx=0.2, rely=0.65, anchor=tk.W)
        # self.lastname_value_label = tk.Label(self, text=self.lastname, foreground=fg, background=bg)
        # self.lastname_value_label.place(relx=0.4, rely=0.65, anchor=tk.W)

        # self.username_label = tk.Label(self, text="Username: ", foreground=fg, background=bg)
        # self.username_label.place(relx=0.2, rely=0.7, anchor=tk.W)
        # self.username_value_label = tk.Label(self, text=self.username, foreground=fg, background=bg)
        # self.username_value_label.place(relx=0.4, rely=0.7, anchor=tk.W)

        # Buttons
        self.course_reg_button = tk.Button(self, text="Course Registration", command=self.course_reg_button_click, padx=20, pady=10, width=20, bg='#87CEEB', font=('Arial', 14, 'bold'))
        self.course_reg_button.place(relx=0.7, rely=0.4, anchor=tk.W)
        self.attendance_button = tk.Button(self, text="Attendance", command=self.attendence_button_click, padx=20, pady=10, width=20, bg='#87CEEB', font=('Arial', 14, 'bold'))
        self.attendance_button.place(relx=0.7, rely=0.5, anchor=tk.W)
        self.grades_button = tk.Button(self, text="Grades", command=self.grades_button_click, padx=20, pady=10, width=20, bg='#87CEEB', font=('Arial', 14, 'bold'))
        self.grades_button.place(relx=0.7, rely=0.6, anchor=tk.W)
        self.logout_button = tk.Button(self, text="Logout", command=self.logout_button_click, bg='#87CEEB', font=('Arial', 10, 'bold'))
        self.logout_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)

    def course_reg_button_click(self):
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\course_reg_instructor.py', username], check=True)
        print("Button 1 clicked")

    def attendence_button_click(self):
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\attendence_try.py', username], check=True)
        print("Button 2 clicked")

    def grades_button_click(self):
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\instructor_grade.py', username], check=True)
        print("Button 3 clicked")
    
    def logout_button_click(self):
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\login_register.py', username], check=True)
        print("Logout button clicked")


# Retrieving the username from command-line arguments
if len(sys.argv) >= 2:
    username = sys.argv[1]
    print(f"Username received in student_dashboard.py: {username}")
else:
    username = 'kumar1v'
app = StudentDashboard(username)
app.mainloop()
