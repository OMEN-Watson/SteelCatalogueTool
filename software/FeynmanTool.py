import tkinter as tk
import json
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import difflib
import sys
import os
import re

# 打包代码：pyinstaller --onefile --windowed --add-data "database.json;." FeynmanTool.py
# C:\Users\GERRY\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pyinstaller.exe --onefile --windowed --add-data "database.json;." FeynmanTool.py
# Path to the JSON file

tempPath = "database.json"
colors = [
    "#FFE4B5",  # Moccasin
    "#D0F0C0",  # Tea Green
    "#ADD8E6",  # Light Sky Blue
    "#E6E6FA",  # Lavender
    "#F0FFF0",  # Honeydew
    "#FFE4E1",  # Misty Rose
    "#E0FFFF",  # Light Cyan
    "#FFFACD",  # Lemon Chiffon
    "#F0F8FF",  # Alice Blue
    "#D8BFD8"   # Thistle
]

# Get the directory where the script is running from
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller bundle
    bundle_dir = sys._MEIPASS
else:
    # Running in development mode
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the JSON file
tempPath = os.path.join(bundle_dir, 'database.json')
steel_data=''

# Load JSON data from file
def load_json(filename=tempPath):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: JSON file '{filename}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: JSON file '{filename}' is not valid.")
        return {}
    
def on_button_click(event):
    left_input = left_entry.get().upper().replace("*", "x").replace("X", "x").strip()
    # Prepare the input numbers list
    # left_input_list = left_input.split()
    # Extract all number substrings using regex
    left_input_list = re.findall(r"\d+", left_input)
    
    # result_text.delete("1.0", tk.END)  # Clear Text widget

    # Determine the steel type (e.g., PFC or SHS)
    steel_type = None
    categories_to_search=[]
    for category in steel_data.keys():
        if category in left_input:
            steel_type = category
            left_input = left_input.replace(category, "")
            categories_to_search = [steel_type]
            break

    if not steel_type:
        letters = re.findall(r'[A-Za-z]+', left_input)
        if len(letters)>0:
            letters=letters[0]
            for category in steel_data.keys(): 
                if letters in category:
                    categories_to_search.append(category)
                    steel_type = category
                    
        

    # Clear previous output
    result_text.delete(0, tk.END)

    # If a specific steel type was detected, search only in that category

    index = 0
    # if steel_type:
        # categories_to_search = [steel_type]
    if not steel_type:
        # If no steel type found, search all
        categories_to_search = steel_data.keys()
    data = [0] * len(categories) 
    # Search for matches
    for category in categories_to_search:
        for section, weight in steel_data[category].items():
            if all(num in section for num in left_input_list):
                result_text.insert(tk.END, f"{section} ({category}): \t {weight} kg/m\n")
             
                result_text.itemconfig(index, bg=colors[categories.index(category)])  # moccasin
                index += 1
                data[categories.index(category)]+=1

    if index == 0:
        result_text.insert(tk.END, "No matching section found.")
    # Display the result in the right input box
    for num in range( len(categories)):
        oneLabel=category_labels[categories[num]]

        if data[num]==0:
             oneLabel.config(bg="SystemButtonFace",borderwidth=0, relief="flat")
        else: oneLabel.config(bg=colors[num],borderwidth=2, relief="solid")

#region label
widget_to_category = {}
def on_label_hover_enter(event):
    widget = event.widget
    # widget.config(bg="gold", font=("Arial", 12, "bold"), relief="raised", bd=1)
    widget.config(bg="gold", font=("Arial", 12), relief="flat", bd=1)



def on_label_hover_leave(event):
    category = widget_to_category[event.widget]
    index = categories.index(category)
    widget = event.widget
    # widget.config(bg=colors[index], font=("Arial", 12, "bold"), relief="flat", bd=0)
    on_button_click(None)  

def label_clicked(event, category):
    current_text = left_entry.get().strip()
    
    # Remove only existing category letters (e.g., PFC, UA) — not numbers like 150x75
    letters = re.sub(r'[A-Za-z]+','',current_text).strip()
    letters += f" {category}"
    left_entry.delete(0, tk.END)
    left_entry.insert(0, letters)
    on_button_click(None)    
#endregion


# Function to copy selected weight to clipboard
def topBoard():
        # Create a frame at the top for the category labels
    label_frame = tk.Frame(root)
    label_frame.pack(pady=5, anchor="n")  # Place it at the top
    # Create individual labels for each category in one horizontal row
    for i, category in enumerate(categories):
        label = tk.Label(label_frame, text=category, bg=colors[i], font=("Arial", 12, "bold"))
        label.pack(side="left", padx=5)
        # bind the click command
        label.bind("<Button-1>", lambda e, cat=category: label_clicked(e, cat))
        category_labels[category] = label  # Store reference

        widget_to_category[label] = category# label animation
        label.bind("<Enter>", on_label_hover_enter)
        label.bind("<Leave>", on_label_hover_leave)
def copy_to_clipboard(event):
    selected = result_text.get(tk.ACTIVE)
    if selected:
        weight = selected.split(": ")[1].split(" ")[1]  # Extract weight number
        root.clipboard_clear()
        root.clipboard_append(weight)
        root.update()
        left_entry.focus_set()

def center_window(win, width=400, height=300):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# 🚨 Clear Button
def clear_input(event):
    left_entry.delete(0, tk.END)
    left_entry.focus_set()

steel_data = load_json(tempPath)
categories = list(steel_data.keys())  # Convert keys to a list
data = [0] * len(categories) 
# Dictionary to hold label references
category_labels = {}

# Create the main window
root = tk.Tk()

center_window(root, 400, 300)
root.title("Feynman Tool")
root.geometry("400x300")  # Width x Height
# Create keywords label
topBoard()

# Create a frame to hold the input boxes and the button
frame = tk.Frame(root)
frame.pack(pady=5)
root.bind("<Escape>", clear_input)

# Create and place the left input box
left_entry = tk.Entry(frame, width=20)
left_entry.grid(row=0, column=0, padx=10)  # Left position in the grid
left_entry.bind("<KeyRelease>", on_button_click)  # Bind key release event
left_entry.focus_set()

# 🚨 Clear Button

# clear_button = tk.Button(frame, text="Clear", command=clear_input)
# clear_button.grid(row=0, column=5, padx=5)

# Scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)




# Create output label and text box for results on the right
# right_label = tk.Label(root, text="Matching Results:")
# right_label.pack()
result_text = tk.Listbox(root, height=10, width=40, font=("Arial", 12),yscrollcommand=scrollbar.set)
result_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
scrollbar.config(command=result_text.yview)
result_text.bind("<Double-Button-1>", copy_to_clipboard)  # Copy on double-click

# Create a button to trigger the action
# button = tk.Button(root, text="Submit", command=on_button_click)
# button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
