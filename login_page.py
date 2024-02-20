import tkinter as tk
from tkinter import messagebox

def switch_to_login_page():
    register_frame.forget()
    login_frame.pack()

def generate_username():
    first_name = register_first_name_entry.get()
    last_name = login_password_entry.get()
    # Take the first 5 letters of the last name, or all letters if less than 5
    username = last_name[:5].lower()

    # If the last name has fewer than 5 letters, add letters from the first name
    if len(username) < 5:
        remaining_letters = 5 - len(username)
        username += first_name[:remaining_letters].lower()

    # Add the number 1
    username += "1"

    # Add the first letter of the first name
    username += first_name[0].lower()

    return username

def switch_to_register_page():
    login_frame.forget()
    register_frame.pack()

def toggle_class_field(*args):
    role = register_role_var.get()

    # Show class field only if the role is "Student"
    if role == "Student":
        register_class_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        register_class_dropdown.grid(row=3, column=1, padx=10, pady=10)
    else:
        register_class_label.grid_forget()
        register_class_dropdown.grid_forget()

def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    # Add your authentication logic here
    # For simplicity, just display a messagebox with login information
    messagebox.showinfo("Login", f"Logged in as {username}")

def register():
    first_name = register_first_name_entry.get()
    last_name = register_last_name_entry.get()
    role = register_role_var.get()
    class_selected = register_class_var.get() if role == "Student" else None
    # username = register_username_entry.get()
    username = generate_username()
    password = register_password_entry.get()

    # Add your registration logic here
    # For simplicity, just display a messagebox with registration information
    info_message = f"Registration Details:\n\nFirst Name: {first_name}\nLast Name: {last_name}\nRole: {role}"

    if class_selected:
        info_message += f"\nClass: {class_selected}"

    info_message += f"\nUsername: {username}\nPassword: {password}"

    messagebox.showinfo("Registration", info_message)
    
    messagebox.showinfo("Generated Username", f"Generated username: {username}")
    # After successful registration, switch back to the login page
    switch_to_login_page()

if __name__ == "__main__":
# def login_page():
    # Create the main window
    root = tk.Tk()
    root.title("Login and Register Pages")

    # Login Page
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
# def register_page():
    # Register Page
    register_frame = tk.Frame(root)

    register_first_name_label = tk.Label(register_frame, text="First Name:")
    register_first_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    register_first_name_entry = tk.Entry(register_frame)
    register_first_name_entry.grid(row=0, column=1, padx=10, pady=10)

    register_last_name_label = tk.Label(register_frame, text="Last Name:")
    register_last_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    register_last_name_entry = tk.Entry(register_frame)
    register_last_name_entry.grid(row=1, column=1, padx=10, pady=10)

    register_role_label = tk.Label(register_frame, text="Role:")
    register_role_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    roles = ["Instructor","Student"]
    register_role_var = tk.StringVar(register_frame)
    register_role_var.set(roles[0])  # Default role is Student

    register_role_var.trace_add("write", toggle_class_field)  # Add a trace to call toggle_class_field when role changes

    register_role_dropdown = tk.OptionMenu(register_frame, register_role_var, *roles)
    register_role_dropdown.grid(row=2, column=1, padx=10, pady=10)
    
    register_class_var = tk.StringVar(register_frame)
    register_class_label = tk.Label(register_frame, text="Class:")
    register_class_dropdown = tk.OptionMenu(register_frame, register_class_var, *["9th", "10th", "11th", "12th"])

    # register_class_label = tk.Label(register_frame, text="Class:")
    # register_class_dropdown = tk.OptionMenu(register_frame, tk.StringVar(register_frame), *["9th", "10th", "11th", "12th"])
    # register_username_label = tk.Label(register_frame, text="Username:")
    # register_username_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

    # register_username_label = tk.Label(register_frame, text=generate_username())
    # register_username_label.grid(row=4, column=1, padx=10, pady=10)

    register_password_label = tk.Label(register_frame, text="Password:")
    register_password_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

    register_password_entry = tk.Entry(register_frame, show="*")
    register_password_entry.grid(row=4, column=1, padx=10, pady=10)

    register_button = tk.Button(register_frame, text="Register", command=register)
    register_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Initially show the login frame
    switch_to_login_page()

    # Start the Tkinter event loop
    root.mainloop()
