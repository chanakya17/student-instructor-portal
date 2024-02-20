import tkinter as tk
from tkinter import ttk
# class get_details():
    

def button1_click():
    # Add functionality for button 1
    print("Button 1 clicked")

def button2_click():
    # Add functionality for button 2
    print("Button 2 clicked")

def button3_click():
    # Add functionality for button 3
    print("Button 3 clicked")

def button4_click():
    # Add functionality for button 4
    print("Button 4 clicked")

# Create the main window
root = tk.Tk()
root.title("Student Details")

# Load an image (replace 'your_image_path.jpg' with the actual path to your image)
# image_path = "E:/cmu/BIS 698/tkinter/Taste of Telangan.png"
image_path = "E:/cmu/BIS 698/698 project/Taste of Telangan.png"
image = tk.PhotoImage(file=image_path)

# Create a label to display the image
image_label = tk.Label(root, image=image)
image_label.pack()

# Frame for student details
details_frame = ttk.Frame(root)
details_frame.pack(pady=10)

# Labels and entry widgets for student details
ttk.Label(details_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
sd_first_name_label = ttk.Label(details_frame, text="Role:")
sd_first_name_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

ttk.Label(details_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
sd_last_name_label = ttk.Label(details_frame, text="Role:")
sd_last_name_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

ttk.Label(details_frame, text="Class:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
sd_class_label = ttk.Label(details_frame, text="Role:")
sd_class_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

ttk.Label(details_frame, text="Username:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
sd_username_label = ttk.Label(details_frame, text="Role:")
sd_username_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")



# Frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack()

# Buttons
button1 = ttk.Button(button_frame, text="Button 1", command=button1_click)
button1.grid(row=0, column=0, padx=5, pady=5)

button2 = ttk.Button(button_frame, text="Button 2", command=button2_click)
button2.grid(row=0, column=1, padx=5, pady=5)

button3 = ttk.Button(button_frame, text="Button 3", command=button3_click)
button3.grid(row=0, column=2, padx=5, pady=5)

button4 = ttk.Button(button_frame, text="Button 4", command=button4_click)
button4.grid(row=0, column=3, padx=5, pady=5)

# Run the Tkinter main loop
root.mainloop()
