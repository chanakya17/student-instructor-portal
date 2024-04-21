import tkinter as tk
import subprocess
import sys
from database import User
from tkinter import font

class AdminDashboard(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title("Admin Dashboard")
        self.state('zoomed')
        self.geometry("900x600")
        self.configure(bg="#00415a")
        self.user = User()
        self.username = username
        self.firstname = self.user.get_details('first_name', username)
        self.lastname = self.user.get_details('last_name', username)
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
        self.firstname_label = tk.Label(self, text=('Welcome'+' '+self.firstname +' '+ self.lastname), 
                                        foreground=fg,
                                        background=bg,
                                        font=custom_font)
        self.firstname_label.place(relx=0.05, rely=0.4, anchor=tk.W)

        # Buttons
        course_button = tk.Button(self, text="Courses", command=self.open_courses, padx=20, pady=10, width=20, bg='#87CEEB', font=('Arial', 14, 'bold'))
        course_button.place(relx=0.6, rely=0.6, anchor=tk.W)

        sections_button = tk.Button(self, text="Sections", command=self.open_sections, padx=20, pady=10, width=20, bg='#87CEEB', font=('Arial', 14, 'bold'))
        sections_button.place(relx=0.6, rely=0.7, anchor=tk.W)
        # Logout Button
        logout_button = tk.Button(self, text="Logout", command=self.logout, bg='#87CEEB', font=('Arial', 10, 'bold'))
        logout_button.place(relx=0.89, rely=0.9, relwidth=0.1, relheight=0.05)

    def open_courses(self):
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\admin_course.py', self.username], check=True)

    def open_sections(self):    
        self.destroy()
        subprocess.run(['python', r'E:\cmu\BIS 698\misc code\admin_section.py', self.username], check=True)

    def logout(self):
        self.destroy()  # Close the current window
        subprocess.run(['python', 'E:\cmu\BIS 698\misc code\login_register.py'])

# Retrieve the username from command-line arguments
if len(sys.argv) >= 2:
    username = sys.argv[1]
    print(f"Username received in admin_dashboard.py: {username}")
else:
    username = 'mechi1c'

# Create an instance of the AdminDashboard class
app = AdminDashboard(username)

# Run the Tkinter main loop
app.mainloop()
