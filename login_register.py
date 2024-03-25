import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3
import subprocess

# Create a connection to the SQLite database
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

# Create a table for user information if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role TEXT NOT NULL,
        class TEXT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()
def clear_entry_boxes():
    login_username_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)
    register_first_name_entry.delete(0, tk.END)
    register_last_name_entry.delete(0, tk.END)
    register_password_entry.delete(0, tk.END)
    # Add additional entries if needed

def switch_to_login_page():
    register_frame.forget()
    login_frame.pack()

def generate_username():
    first_name = register_first_name_entry.get()
    last_name = register_last_name_entry.get()
    username = last_name[:5].lower()

    if len(username) < 5:
        remaining_letters = 5 - len(username)
        username += first_name[:remaining_letters].lower()

    username += "1"
    username += first_name[0].lower()

    return username

def switch_to_register_page():
    login_frame.forget()
    register_frame.pack()

def toggle_class_field(*args):
    role = register_role_var.get()

    if role == "Student":
        register_class_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        register_class_dropdown.grid(row=3, column=1, padx=10, pady=10)
    else:
        register_class_label.grid_forget()
        register_class_dropdown.grid_forget()

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
        print(role)
        if role == 'Student':
            subprocess.run(['python', 'E:\cmu\BIS 698\misc code\student_dashboard.py', username], check=True)
        elif role == 'Instructor':
            subprocess.run(['python', 'E:\cmu\BIS 698\misc code\instructor_dashboard.py', username], check=True)
        else:
            subprocess.run(['python', 'E:\cmu\BIS 698\misc code\admin_dashboard.py', username], check=True)
    else:
        messagebox.showerror("Error", "Invalid username or password")
    
    

def register():
    first_name = register_first_name_entry.get()
    last_name = register_last_name_entry.get()
    role = register_role_var.get()
    class_selected = register_class_var.get() if role == "Student" else None
    password = register_password_entry.get()
    if any((entry_value is None or entry_value == '') for entry_value in [first_name, last_name, role, password]):
        messagebox.showerror("Error", "Please fill in all the required fields.")
        return  # Exit the function if any entry is missing
    username = generate_username()
    print(username)
    clear_entry_boxes()
    try:
        cursor.execute('''
            INSERT INTO users (first_name, last_name, role, class, user_id, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, role, class_selected, username, password))
        conn.commit()

        messagebox.showinfo("Registration", "Registration successful!")
        messagebox.showinfo("Generated Username", f"Generated username: {username}")
        switch_to_login_page()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login and Register Pages")
#loginframe
    login_frame = tk.Frame(root)

    login_username_label = tk.Label(login_frame, text="Username:")
    login_username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    login_username_entry = tk.Entry(login_frame)
    login_username_entry.grid(row=0, column=1, padx=10, pady=10)

    login_password_label = tk.Label(login_frame, text="Password:")
    login_password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    login_password_entry = tk.Entry(login_frame, show="*")
    login_password_entry.grid(row=1, column=1, padx=10, pady=10)

    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    register_button = tk.Button(login_frame, text="Register", command=switch_to_register_page)
    register_button.grid(row=3, column=0, columnspan=2, pady=10)
#registerframe
    register_frame = tk.Frame(root)

    register_first_name_label = ttk.Label(register_frame, text="First Name:")
    register_first_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    register_first_name_entry = ttk.Entry(register_frame)
    register_first_name_entry.grid(row=0, column=1, padx=10, pady=10)

    register_last_name_label = ttk.Label(register_frame, text="Last Name:")
    register_last_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    register_last_name_entry = ttk.Entry(register_frame)
    register_last_name_entry.grid(row=1, column=1, padx=10, pady=10)

    register_role_label = ttk.Label(register_frame, text="Role:")
    register_role_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    roles = ["Instructor", "Student", "Admin"]
    register_role_var = tk.StringVar(register_frame)
    register_role_var.set(roles[0])

    register_role_var.trace_add("write", toggle_class_field)

    register_role_dropdown = ttk.Combobox(register_frame, textvariable=register_role_var, values=roles)
    register_role_dropdown.grid(row=2, column=1, padx=10, pady=10)

    register_class_var = tk.StringVar(register_frame)
    register_class_label = tk.Label(register_frame, text="Class:")
    register_class_var.set("9th")
    register_class_dropdown = ttk.Combobox(register_frame, textvariable=register_class_var, values=["9th", "10th", "11th", "12th"])

    register_password_label = ttk.Label(register_frame, text="Password:")
    register_password_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

    register_password_entry = ttk.Entry(register_frame, show="*")
    register_password_entry.grid(row=4, column=1, padx=10, pady=10)

    register_button = ttk.Button(register_frame, text="Register", command=register)
    register_button.grid(row=5, column=0, columnspan=2, pady=10)

    switch_to_login_page()

    root.mainloop()

# Close the database connection when the application exits
conn.close()
