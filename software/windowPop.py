import tkinter as tk
import json
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import difflib
import sys
import os

# 打包代码：pyinstaller --onefile --windowed --add-data "database.json;." windowPop.py
# C:\Users\GERRY\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pyinstaller.exe --onefile --windowed --add-data "database.json;." windowPop.py
# Path to the JSON file

tempPath = "database.json"

# Get the directory where the script is running from
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller bundle
    bundle_dir = sys._MEIPASS
else:
    # Running in development mode
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the JSON file
tempPath = os.path.join(bundle_dir, 'database.json')
steel_data='';

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
    
# Function to process input and update the right input box
def on_button_click(event):
   left_input  = left_entry.get().upper().replace(" ", "").replace("*", "x").replace("X", "x").strip()
   matched_items = []
    # Check for category (PFC or SHS)
   steel_type = None
   for category in steel_data.keys():
        if category in left_input:
            steel_type = category
            left_input = left_input.replace(category, "")
            break
   if not steel_type:
        result_text.delete(0, tk.END)
        result_text.insert(0, "Steel type not found.")
        return 
   
    #region 
    # Use fuzzy matching to find the closest matches for the cleaned input
   sizes = list(steel_data[steel_type].keys())
   # Find top 5 closest matches
   matches = difflib.get_close_matches(left_input, sizes, n=20, cutoff=0.3)  
       # Format the result as a vertical list
   result_text.delete(0, tk.END)

   if matches:
        for match in matches:
            if isinstance(steel_data[category][match], dict):
                for thickness, weight in steel_data[category][match].items():
                    result_text.insert(tk.END, f"{match} {thickness}: **{weight} kg/m**\n")
            else:
                result_text.insert(tk.END, f"{match}: {steel_data[category][match]} kg/m\n")
   else:
        result_text.insert(tk.END, "No close matches found")
          #endregion



    # Check if the dimension exists in the selected steel type
#    if left_input in steel_data[steel_type]:
#         weight = steel_data[steel_type][left_input]
#         result = f"Weight: {weight} kg/m"
#    else:
#         result = "Dimension not found."
    
    # Display the result in the right input box
# Function to copy selected weight to clipboard
def topBoard():
    text=''
    for category in steel_data.keys():
        text+=f"{category}  "
    return text
def copy_to_clipboard(event):
    selected = result_text.get(tk.ACTIVE)
    if selected:
        weight = selected.split(": ")[1].split(" ")[0]  # Extract weight number
        root.clipboard_clear()
        root.clipboard_append(weight)
        root.update()



steel_data = load_json(tempPath)
# Create the main window
root = tk.Tk()
root.title("Custom Window with Input Boxes")
root.geometry("400x300")  # Width x Height

# Create a frame to hold the input boxes and the button
frame = tk.Frame(root)
frame.pack(pady=20)

# Create and place the left input box
left_entry = tk.Entry(frame, width=20)
left_entry.grid(row=0, column=0, padx=10)  # Left position in the grid
left_entry.bind("<KeyRelease>", on_button_click)  # Bind key release event
left_entry.focus_set()
# Scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Create keywords label
text=topBoard()
keywords_label = tk.Label(root, text=text)
keywords_label.pack()
# Create output label and text box for results on the right
right_label = tk.Label(root, text="Matching Results:")
right_label.pack()
result_text = tk.Listbox(root, height=10, width=40,yscrollcommand=scrollbar.set)
result_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
scrollbar.config(command=result_text.yview)
result_text.bind("<Double-Button-1>", copy_to_clipboard)  # Copy on double-click

# Create a button to trigger the action
# button = tk.Button(root, text="Submit", command=on_button_click)
# button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
