import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create a connection to the SQLite database
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

def clear_entry_boxes():
    login_username_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)
    register_first_name_entry.delete(0, tk.END)
    register_last_name_entry.delete(0, tk.END)
    register_password_entry.delete(0, tk.END)
    register_email_entry.delete(0, tk.END)  # Clear email entry

def switch_to_login_page():
    register_frame.place_forget()
    login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    clear_entry_boxes()

def generate_username():
    firstname = register_first_name_entry.get()
    lastname = register_last_name_entry.get()

    if len(lastname) >= 5:
        user_id = lastname[:5] + '1' + firstname[0]
    else:
        user_id = lastname + (firstname[:5 - len(lastname)] if len(firstname) >= 5 - len(lastname) else firstname) + '1' + firstname[0]
    
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()
    while existing_user:
        i = int(user_id[-2]) + 1
        user_id = user_id[:-2] + str(i) + firstname[0]
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        existing_user = cursor.fetchone()

    return user_id

def switch_to_register_page():
    login_frame.place_forget()
    register_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    clear_entry_boxes()

def toggle_class_field(*args):
    role = register_role_var.get()

    if role == "Student":
        register_class_label.place(relx=0.4, rely=0.525)
        register_class_dropdown.place(relx=0.5, rely=0.525)
        register_email_label.place(relx=0.4, rely=0.6)
        register_email_entry.place(relx=0.5, rely=0.6)
        register_password_label.place(relx=0.4, rely=0.675)
        register_password_entry.place(relx=0.5, rely=0.675)
        register_button.place(relx=0.45, rely=0.75)
        back_button.place(relx=0.5, rely=0.75)
    else:
        register_email_label.place(relx=0.4, rely=0.525)
        register_email_entry.place(relx=0.5, rely=0.525)
        register_password_label.place(relx=0.4, rely=0.6)
        register_password_entry.place(relx=0.5, rely=0.6)
        back_button.place(relx=0.5, rely=0.675)
        register_button.place(relx=0.45, rely=0.675)
        register_class_label.place_forget()
        register_class_dropdown.place_forget()

def login():
    username = login_username_entry.get()
    password = login_password_entry.get()
    clear_entry_boxes()
    cursor.execute('''
        SELECT * FROM users WHERE user_id = ? AND password = ?
    ''', (username, password))

    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login", f"Logged in as {username}")
        root.destroy()
        cursor.execute("SELECT role FROM users WHERE user_id = ?",(username,))
        result=cursor.fetchone()
        role = result[0]
        if role == 'Student':
            subprocess.run(['python', 'student_dashboard.py', username], check=True)
        elif role == 'Instructor':
            subprocess.run(['python', 'instructor_dashboard.py', username], check=True)
        else:
            subprocess.run(['python', 'admin_dashboard.py', username], check=True)
    else:
        messagebox.showerror("Error", "Invalid username or password")

def register():
    first_name = register_first_name_entry.get().title()
    last_name = register_last_name_entry.get().title()
    role = register_role_var.get()
    class_selected = register_class_var.get() if role == "Student" else None
    password = register_password_entry.get()
    email = register_email_entry.get()  # Get email from the entry widget
    if any((entry_value is None or entry_value == '') for entry_value in [first_name, last_name, role, password, email]):
        messagebox.showerror("Error", "Please fill in all the required fields.")
        return
    # Define the regex patterns for password validation
    regex_length = r".{6,}"
    regex_symbol = r"[!@#$%^&*(),.?\":{}|<>]"
    regex_uppercase = r"[A-Z]"

    # Check if password meets all the requirements
    error_messages = []
    if not re.search(regex_length, password):
        error_messages.append("Password must be at least 6 characters long.")
    if not re.search(regex_symbol, password):
        error_messages.append("Password must contain at least one symbol.")
    if not re.search(regex_uppercase, password):
        error_messages.append("Password must have at least one uppercase character.")

    if error_messages:
        messagebox.showerror("Error", "\n".join(error_messages))
        return
    
    username = generate_username()
    clear_entry_boxes()

    cursor.execute('''
        INSERT INTO users (first_name, last_name, role, class, user_id, password, email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, role, class_selected, username, password, email))  # Include email in the insert query
    conn.commit()

    # Send email to the user with the generated username
    send_email(email, username,first_name,last_name)

    messagebox.showinfo("Registration", "Registration successful!")
    messagebox.showinfo("Generated Username", f"Generated username: {username}")
    switch_to_login_page()

def send_email(receiver_email, username,first_name,last_name):
    try:
        sender_email = ""  # Your email address
        smtp_server = "smtp.gmail.com"  # Your SMTP server address
        smtp_port = 587  # Your SMTP port
        smtp_username = sender_email  # Your SMTP username
        smtp_password = ""  # Your SMTP password

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Registration Successful"
        
        body = f"Dear {first_name} {last_name},\n\nYour registration was successful. Your username is: {username}\n\nBest Regards,\nCMU High School"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login and Register Pages")
    root.state('zoomed')
    root.geometry("900x600")
    root.configure(bg="#00415a")
    image_path = "E:/cmu/BIS 698/misc code/cmu high scl.png"
    img = tk.PhotoImage(file=image_path)
    image2_path =  "E:/cmu/BIS 698/misc code/OIG2.png"
    img2 = tk.PhotoImage(file=image2_path)

    # login frame
    login_frame = tk.Frame(root, bg="#00415a")
    login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    image_label = tk.Label(login_frame, image=img)
    image_label.place(relx=0.5, rely=0.0, anchor=tk.N)
    login_username_label = tk.Label(login_frame, text="Username:", bg="#00415a", fg="white")
    login_username_label.place(relx=0.4, rely=0.35)

    login_username_entry = tk.Entry(login_frame)
    login_username_entry.place(relx=0.5, rely=0.35)

    login_password_label = tk.Label(login_frame, text="Password:", bg="#00415a", fg="white")
    login_password_label.place(relx=0.4, rely=0.4)

    login_password_entry = tk.Entry(login_frame, show="*")
    login_password_entry.place(relx=0.5, rely=0.4)

    login_button = tk.Button(login_frame, text="Login", command=login, bg='#87CEEB')
    login_button.place(relx=0.45, rely=0.45)

    register_button = tk.Button(login_frame, text="Register", command=switch_to_register_page, bg='#87CEEB')
    register_button.place(relx=0.51, rely=0.45)

    # register frame
    register_frame = tk.Frame(root, bg="#00415a")
    register_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    image_label = tk.Label(register_frame, image=img)
    image_label.place(relx=0.5, rely=0.0, anchor=tk.N)

    register_first_name_label = ttk.Label(register_frame, text="First Name:", background="#00415a", foreground="white")
    register_first_name_label.place(relx=0.4, rely=0.3)

    register_first_name_entry = ttk.Entry(register_frame)
    register_first_name_entry.place(relx=0.5, rely=0.3)

    register_last_name_label = ttk.Label(register_frame, text="Last Name:", background="#00415a", foreground="white")
    register_last_name_label.place(relx=0.4, rely=0.375)

    register_last_name_entry = ttk.Entry(register_frame)
    register_last_name_entry.place(relx=0.5, rely=0.375)

    register_role_label = ttk.Label(register_frame, text="Role:", background="#00415a", foreground="white")
    register_role_label.place(relx=0.4, rely=0.45)

    roles = ["Instructor", "Student", "Admin"]
    register_role_var = tk.StringVar(register_frame)
    register_role_var.set(roles[0])

    register_role_var.trace_add("write", toggle_class_field)

    register_role_dropdown = ttk.Combobox(register_frame, textvariable=register_role_var, values=roles)
    register_role_dropdown.place(relx=0.5, rely=0.45)

    register_class_var = tk.StringVar(register_frame)
    register_class_label = ttk.Label(register_frame, text="Class:", background="#00415a", foreground="white")
    register_class_var.set(9)
    register_class_dropdown = ttk.Combobox(register_frame, textvariable=register_class_var, values=[9,10,11,12])

    register_email_label = ttk.Label(register_frame, text="Email:", background="#00415a", foreground="white")
    register_email_label.place(relx=0.4, rely=0.525)

    register_email_entry = ttk.Entry(register_frame)  # Add email entry field
    register_email_entry.place(relx=0.5, rely=0.525)

    register_password_label = ttk.Label(register_frame, text="Password:", background="#00415a", foreground="white")
    register_password_label.place(relx=0.4, rely=0.6)

    register_password_entry = ttk.Entry(register_frame, show="*")
    register_password_entry.place(relx=0.5, rely=0.6)

    register_button = tk.Button(register_frame, text="Register", command=register,bg='#87CEEB')
    register_button.place(relx=0.45, rely=0.675)
    
    back_button = tk.Button(register_frame, text="Back", command=switch_to_login_page,bg='#87CEEB')
    back_button.place(relx=0.5, rely=0.675)
    
    switch_to_login_page()

    root.mainloop()

# Close the database connection 
conn.close()
