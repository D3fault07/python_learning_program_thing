





# i did NOT make this myself
# none of ts was made by me :3

"""
Comprehensive Python Interactive Tutorial
Author: OpenAI ChatGPT
Date: 2024-04-27

This script serves as an extensive interactive Python tutorial covering various topics,
libraries, and functionalities. It utilizes a graphical user interface (GUI) built with
Tkinter to provide an engaging learning experience.

**Note:** Before running this script, ensure that all required external libraries are installed.
You can install missing libraries using pip. For example:
    pip install pyautogui discord.py psutil requests
"""

# ---------------- Standard Library Imports ----------------
import sys
import os
import time
import json
import ctypes
import subprocess
import textwrap
import traceback
import threading
import random
from tkinter import messagebox, scrolledtext, filedialog, ttk
import tkinter as tk

# ---------------- External Library Imports ----------------
# PyAutoGUI for automation
try:
    import pyautogui
except ImportError:
    pyautogui = None
    print("pyautogui is not installed. Install it using 'pip install pyautogui' to enable automation features.")

# Discord.py for Discord bot interactions
try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    print("discord.py is not installed. Install it using 'pip install discord.py' to enable Discord bot features.")

# Psutil for system monitoring
try:
    import psutil
except ImportError:
    psutil = None
    print("psutil is not installed. Install it using 'pip install psutil' to enable system monitoring features.")

# Requests for HTTP requests
try:
    import requests
except ImportError:
    requests = None
    print("requests is not installed. Install it using 'pip install requests' to enable HTTP request features.")

# ---------------- Global Variables ----------------
# Initialize the main Tkinter window
root = tk.Tk()
root.title("Comprehensive Python Interactive Tutorial")
root.geometry("1800x1000")  # Width x Height

# Define global colors and styles
LIGHT_THEME = {
    "bg": "#F0F0F0",
    "fg": "#000000",
    "button_bg": "#4CAF50",
    "button_fg": "#FFFFFF",
    "text_bg": "#FFFFFF",
    "text_fg": "#000000",
    "output_bg": "#000000",
    "output_fg": "#00FF00",
    "highlight_bg": "#D3D3D3",
}

DARK_THEME = {
    "bg": "#2E2E2E",
    "fg": "#FFFFFF",
    "button_bg": "#555555",
    "button_fg": "#FFFFFF",
    "text_bg": "#1E1E1E",
    "text_fg": "#FFFFFF",
    "output_bg": "#1E1E1E",
    "output_fg": "#00FF00",
    "highlight_bg": "#3E3E3E",
}

current_theme = LIGHT_THEME
root.configure(bg=current_theme["bg"])

# Dictionary to store user progress
user_progress = {
    "Introduction": False,
    "Variables & Data Types": False,
    "Control Structures": False,
    "Functions": False,
    "Modules & Packages": False,
    "Object-Oriented Programming": False,
    "File Handling": False,
    "Exception Handling": False,
    "Advanced Topics": False,
    "Quizzes": False,
    "Random Module": False,
    "Time Module": False,
    "OS Module": False,
    "Tkinter Module": False,
    "PyAutoGUI Module": False,
    "Discord Module": False,
    "Requests Module": False,
    "JSON Module": False,
    "ctypes Module": False,
    "psutil Module": False,
    "Subprocess Module": False
}

# List to keep track of quiz-related widgets for theming
quiz_widgets = []

# ---------------- Utility Functions ----------------

def clear_text(text_widget):
    """Clears the content of a scrolled text widget."""
    text_widget.config(state=tk.NORMAL)
    text_widget.delete('1.0', tk.END)
    text_widget.config(state=tk.DISABLED)

def display_text(text_widget, content):
    """Displays content in a scrolled text widget."""
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, content)
    text_widget.config(state=tk.DISABLED)

def gui_input(prompt):
    """Handles input() calls by displaying a simple input dialog in the GUI."""
    from tkinter.simpledialog import askstring
    return askstring("Input Required", prompt)

def execute_code(code):
    """Executes Python code and appends the output or errors to the output box."""
    try:
        import io
        import contextlib

        # Redirect `input` to `gui_input`
        exec_globals = {"input": gui_input}

        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exec(code, exec_globals)
        output = stdout.getvalue()
        errors = stderr.getvalue()

        # Append the new output/errors to the output box
        output_box.config(state=tk.NORMAL)
        if output.strip():
            output_box.insert(tk.END, output + '\n')
        if errors.strip():
            output_box.insert(tk.END, errors + '\n')
        output_box.config(state=tk.DISABLED)
    except Exception as e:
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, f"Error: {str(e)}\n")
        output_box.config(state=tk.DISABLED)

def show_error(message):
    """Displays an error message box."""
    messagebox.showerror("Error", message)

def show_info(message):
    """Displays an information message box."""
    messagebox.showinfo("Information", message)

def check_external_libraries():
    """Checks if all required external libraries are installed."""
    missing_libraries = []
    if pyautogui is None:
        missing_libraries.append("pyautogui")
    if discord is None:
        missing_libraries.append("discord.py")
    if psutil is None:
        missing_libraries.append("psutil")
    if requests is None:
        missing_libraries.append("requests")
    # Add checks for additional libraries here

    if missing_libraries:
        message = "The following libraries are missing:\n" + ", ".join(missing_libraries) + \
                  "\n\nPlease install them using pip before proceeding."
        show_error(message)
        sys.exit(1)

def save_progress():
    """Saves the user progress to a JSON file."""
    try:
        with open('user_progress.json', 'w') as f:
            json.dump(user_progress, f)
    except Exception as e:
        show_error(f"Failed to save progress:\n{e}")

def load_progress():
    """Loads the user progress from a JSON file."""
    global user_progress
    if os.path.exists('user_progress.json'):
        try:
            with open('user_progress.json', 'r') as f:
                user_progress = json.load(f)
        except Exception as e:
            show_error(f"Failed to load progress:\n{e}")

def mark_topic_completed(topic):
    """Marks a topic as completed and saves the progress."""
    user_progress[topic] = True
    save_progress()
    update_nav_buttons()

def update_nav_buttons():
    """Updates the navigation buttons to reflect completed topics."""
    for btn in nav_buttons:
        topic = btn.cget('text')
        if user_progress.get(topic, False):
            btn.config(bg="#6B8E23")  # Dark Olive Green for completed
        else:
            btn.config(bg=current_theme["button_bg"])

def toggle_theme():
    """Toggles between Light and Dark themes."""
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    apply_theme()

def apply_theme():
    """Applies the current theme to all widgets."""
    root.configure(bg=current_theme["bg"])
    
    # Update left frame
    left_frame.configure(bg=current_theme["bg"])
    for btn in nav_buttons:
        btn.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    
    # Update right frame
    right_frame.configure(bg=current_theme["bg"])
    
    # Update content text
    content_text.configure(bg=current_theme["text_bg"], fg=current_theme["text_fg"])
    
    # Update code editor
    code_entry.configure(bg=current_theme["text_bg"], fg=current_theme["text_fg"])
    
    # Update output text
    output_box.configure(bg=current_theme["output_bg"], fg=current_theme["output_fg"])
    
    # Update other widgets
    execute_button.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    save_button.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    load_button.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    theme_button.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    search_btn.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    resources_button.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    feedback_btn.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    
    # Update quiz feedback
    for widget in quiz_widgets:
        widget.configure(bg=current_theme["bg"], fg=current_theme["fg"])

def search_topic():
    """Searches for a topic in the navigation buttons and invokes it."""
    query = search_entry.get().lower()
    for btn in nav_buttons:
        if query in btn.cget('text').lower():
            btn.invoke()
            return
    show_info("No matching topic found.")

def submit_feedback():
    """Submits user feedback by saving it to a file."""
    feedback = feedback_entry.get('1.0', tk.END).strip()
    if feedback:
        try:
            with open('feedback.txt', 'a') as f:
                f.write(feedback + "\n---\n")
            show_info("Thank you for your feedback!")
            feedback_entry.delete('1.0', tk.END)
        except Exception as e:
            show_error(f"Failed to submit feedback:\n{e}")
    else:
        show_error("Please enter some feedback before submitting.")

# ---------------- GUI Components Setup ----------------

# Left Frame for Navigation Buttons
left_frame = tk.Frame(root, width=300, bg=current_theme["bg"])
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Right Frame for Content Display and Code Execution
right_frame = tk.Frame(root, bg=current_theme["bg"])
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Navigation Canvas with Scrollbar
nav_canvas = tk.Canvas(left_frame, bg=current_theme["bg"])
nav_scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=nav_canvas.yview)
nav_scrollable_frame = tk.Frame(nav_canvas, bg=current_theme["bg"])

nav_scrollable_frame.bind(
    "<Configure>",
    lambda e: nav_canvas.configure(
        scrollregion=nav_canvas.bbox("all")
    )
)

nav_canvas.create_window((0, 0), window=nav_scrollable_frame, anchor="nw")
nav_canvas.configure(yscrollcommand=nav_scrollbar.set)
nav_canvas.pack(side="left", fill="both", expand=True)
nav_scrollbar.pack(side="right", fill="y")

# List to keep track of navigation buttons
nav_buttons = []

def create_nav_button(parent, text, command):
    """Creates and packs a navigation button."""
    btn = tk.Button(
        parent, text=text, width=35,
        bg=current_theme["button_bg"], fg=current_theme["button_fg"],
        command=command, anchor='w', justify='left',
        font=('Arial', 12)
    )
    btn.pack(pady=5, padx=10, fill=tk.X)
    nav_buttons.append(btn)

# Define Navigation Topics
topics = [
    "Introduction",
    "Variables & Data Types",
    "Control Structures",
    "Functions",
    "Modules & Packages",
    "Object-Oriented Programming",
    "File Handling",
    "Exception Handling",
    "Advanced Topics",
    "Quizzes",
    "Random Module",
    "Time Module",
    "OS Module",
    "Tkinter Module",
    "PyAutoGUI Module",
    "Discord Module",
    "Requests Module",
    "JSON Module",
    "ctypes Module",
    "psutil Module",
    "Subprocess Module",
    "Resources",
    "Toggle Theme",
    "Exit"
]

# Create Navigation Buttons
for topic in topics:
    if topic == "Toggle Theme":
        create_nav_button(nav_scrollable_frame, "Toggle Theme", toggle_theme)
    elif topic == "Exit":
        create_nav_button(nav_scrollable_frame, "Exit", lambda: root.quit())
    else:
        create_nav_button(nav_scrollable_frame, topic, lambda t=topic: load_topic(t))

# Content Text Widget
content_text = scrolledtext.ScrolledText(
    right_frame, wrap=tk.WORD,
    bg=current_theme["text_bg"], fg=current_theme["text_fg"],
    state=tk.DISABLED, font=('Arial', 14)
)
content_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Code Editor Label
code_entry_label = tk.Label(
    right_frame, text="Code Editor:",
    bg=current_theme["bg"], fg=current_theme["fg"],
    font=('Arial', 12, 'bold')
)
code_entry_label.pack(padx=20, anchor='w')

# Code Editor Widget
code_entry = scrolledtext.ScrolledText(
    right_frame, height=20, wrap=tk.WORD,
    bg=current_theme["text_bg"], fg=current_theme["text_fg"],
    font=('Consolas', 12)
)
code_entry.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

# Auto-closing brackets and quotes
def on_key_press(event):
    opening = "([{"
    closing = ")]}"
    pair = {'(': ')', '[': ']', '{': '}'}

    if event.char in pair:
        index = code_entry.index(tk.INSERT)
        code_entry.insert(tk.INSERT, pair[event.char])
        code_entry.mark_set(tk.INSERT, f"{index}+1c")
    elif event.char in "'\"":
        index = code_entry.index(tk.INSERT)
        code_entry.insert(tk.INSERT, event.char)
        code_entry.mark_set(tk.INSERT, f"{index}+1c")
#DO NOT UNCOMMENT TS TS WILL BREAK EVERYTHING IN THE CODE EDITOR
#code_entry.bind("<KeyPress>", on_key_press)

# Output Box Label
output_label = tk.Label(
    left_frame, text="Output:", font=('Arial', 12),
    bg=current_theme["bg"], fg=current_theme["fg"]
)
output_label.pack(pady=10, anchor="w")

# Output Box Widget
output_box = scrolledtext.ScrolledText(
    left_frame, wrap=tk.WORD, height=10,
    bg=current_theme["text_bg"], fg=current_theme["text_fg"],
    font=('Consolas', 12), state=tk.DISABLED
)
output_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Execute and Clear Buttons Frame
button_frame = tk.Frame(left_frame, bg=current_theme["bg"])
button_frame.pack(pady=5)

execute_button = tk.Button(
    button_frame, text="Run Code",
    bg="#4CAF50", fg="#FFFFFF",
    font=('Arial', 12, 'bold'), width=15, height=2,
    command=lambda: execute_code(code_entry.get('1.0', tk.END))
)
execute_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(
    button_frame, text="Clear Output",
    bg="#FF5733", fg="#FFFFFF",
    font=('Arial', 12, 'bold'), width=15, height=2,
    command=lambda: clear_output()
)
clear_button.pack(side=tk.LEFT, padx=5)

def clear_output():
    """Clears the content of the output_box."""
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.config(state=tk.DISABLED)

# Save and Load Code Functions
def save_code():
    """Saves the code from the editor to a file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'w') as file:
                code = code_entry.get('1.0', tk.END)
                file.write(code)
            show_info("Code saved successfully!")
        except Exception as e:
            show_error(f"Failed to save code:\n{e}")

def load_code():
    """Loads code from a file into the editor."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r') as file:
                code = file.read()
                code_entry.delete('1.0', tk.END)
                code_entry.insert(tk.END, code)
            show_info("Code loaded successfully!")
        except Exception as e:
            show_error(f"Failed to load code:\n{e}")

# Save and Load Buttons Frame
code_buttons_frame = tk.Frame(right_frame, bg=current_theme["bg"])
code_buttons_frame.pack(pady=5, padx=20, anchor='e')

save_button = tk.Button(
    code_buttons_frame, text="Save Code",
    bg=current_theme["button_bg"], fg=current_theme["button_fg"],
    command=save_code, font=('Arial', 12)
)
save_button.pack(side=tk.LEFT, padx=5)

load_button = tk.Button(
    code_buttons_frame, text="Load Code",
    bg=current_theme["button_bg"], fg=current_theme["button_fg"],
    command=load_code, font=('Arial', 12)
)
load_button.pack(side=tk.LEFT, padx=5)

# Search Functionality Setup
def setup_search():
    """Sets up the search bar in the navigation pane."""
    search_frame = tk.Frame(left_frame, bg=current_theme["bg"])
    search_frame.pack(pady=10, padx=10, fill=tk.X)

    search_entry_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_entry_var, font=('Arial', 12))
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))

    search_btn = tk.Button(
        search_frame, text="Search",
        command=search_topic, font=('Arial', 12),
        bg=current_theme["button_bg"], fg=current_theme["button_fg"]
    )
    search_btn.pack(side=tk.LEFT)

    return search_entry, search_btn

search_entry, search_btn = setup_search()

# Feedback Section
feedback_label = tk.Label(
    right_frame, text="Feedback:",
    bg=current_theme["bg"], fg=current_theme["fg"],
    font=('Arial', 12)
)
feedback_label.pack(pady=5)

feedback_entry = tk.Text(
    right_frame, height=5, wrap=tk.WORD,
    bg=current_theme["text_bg"], fg=current_theme["text_fg"],
    font=('Consolas', 12)
)
feedback_entry.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

feedback_btn = tk.Button(
    right_frame, text="Submit Feedback",
    bg=current_theme["button_bg"], fg=current_theme["button_fg"],
    command=submit_feedback, font=('Arial', 12)
)
feedback_btn.pack(pady=5)

# ---------------- Topic Functions ----------------

def load_topic(topic):
    """Loads the content for a given topic."""
    topic_functions = {
        "Introduction": introduction,
        "Variables & Data Types": variables_data_types,
        "Control Structures": control_structures,
        "Functions": functions,
        "Modules & Packages": modules_packages,
        "Object-Oriented Programming": oop,
        "File Handling": file_handling,
        "Exception Handling": exception_handling,
        "Advanced Topics": advanced_topics,
        "Quizzes": quizzes,
        "Random Module": random_module,
        "Time Module": time_module,
        "OS Module": os_module,
        "Tkinter Module": tkinter_module,
        "PyAutoGUI Module": pyautogui_module,
        "Discord Module": discord_module,
        "Requests Module": requests_module,
        "JSON Module": json_module,
        "ctypes Module": ctypes_module,
        "psutil Module": psutil_module,
        "Subprocess Module": subprocess_module,
        "Resources": show_resources
    }
    
    func = topic_functions.get(topic, placeholder_function)
    func()
    mark_topic_completed(topic)

# ---------------- Topic Content Functions ----------------

def introduction():
    """Displays the Introduction content."""
    clear_text(content_text)
    intro_content = textwrap.dedent("""
        # Introduction to Python

        Python is a high-level, interpreted programming language known for its readability and versatility. It supports multiple programming paradigms, including procedural, object-oriented, and functional programming.

        ## History of Python
        Python was created by Guido van Rossum and first released in 1991. It was designed to emphasize code readability and simplicity.

        ## Features of Python
        - Simple and Easy to Learn
        - Interpreted Language
        - Dynamically Typed
        - Extensive Standard Library
        - Supports Multiple Programming Paradigms
        - Strong Community Support

        ## Installing Python
        1. Download Python from the official website: [python.org](https://docs.python.org/3/)
        2. Choose the installer that matches your operating system.
        3. Run the installer and follow the on-screen instructions.
        4. Verify the installation by opening a terminal or command prompt and typing:
           ```
           python --version
           ```

        ## Writing Your First Python Program
        Let's write a simple Python program that prints 'Hello, World!'.

        ```python
        print('Hello, World!')
        ```

        ## Try It Yourself
        Enter the above code in the code editor below and click "Run Code" to see the output.
    """)
    display_text(content_text, intro_content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, "print('Hello, World!')")

def variables_data_types():
    """Displays the Variables and Data Types content."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # Variables and Data Types

        In Python, variables are used to store data. You don't need to declare their type explicitly.

        ## Variables
        Variables are created when you assign a value to them.
        ```python
        x = 5
        y = 'Hello'
        z = 3.14
        ```

        Variables can be reassigned to different types:
        ```python
        x = 'Now I\'m a string!'
        ```

        ## Data Types
        - **Integers (`int`)**: Whole numbers, e.g., `1`, `-3`, `42`
        - **Floating-point numbers (`float`)**: Decimal numbers, e.g., `3.14`, `-0.001`
        - **Strings (`str`)**: Text, e.g., `'Hello, World!'`
        - **Booleans (`bool`)**: `True` or `False`
        - **Lists**: Ordered, mutable collections, e.g., `[1, 2, 3]`
        - **Tuples**: Ordered, immutable collections, e.g., `(1, 2, 3)`
        - **Dictionaries**: Key-value pairs, e.g., `{'name': 'Alice', 'age': 25}`

        ## Type Conversion
        You can convert between data types using functions like `int()`, `float()`, `str()`, etc.
        ```python
        x = '5'
        y = int(x) + 10  # y becomes 15
        ```

        ## Basic Input/Output
        - **Input**: Get user input using `input()`.
        - **Output**: Display output using `print()`.
        ```python
        name = input('Enter your name: ')
        print('Hello, ' + name + '!')
        ```

        ## Try It Yourself
        Experiment with variables and data types in the code editor below.
    """)
    display_text(content_text, content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
# Define variables
a = 10
b = 20
c = a + b
print('Sum of a and b:', c)
""")

def control_structures():
    """Displays the Control Structures content."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # Control Structures

        Control structures allow you to control the flow of your program.

        ## If Statements
        ```python
        age = 18
        if age >= 18:
            print('You are an adult.')
        else:
            print('You are a minor.')
        ```

        ## For Loops
        ```python
        for i in range(5):
            print(i)
        ```

        ## While Loops
        ```python
        count = 0
        while count < 5:
            print(count)
            count += 1
        ```

        ## Break and Continue
        - `break`: Exit the nearest enclosing loop.
        - `continue`: Skip the rest of the current loop iteration and continue with the next one.
        ```python
        for i in range(10):
            if i == 5:
                break
            print(i)

        for i in range(10):
            if i % 2 == 0:
                continue
            print(i)
        ```

        ## Try It Yourself
        Write an `if` statement, `for` loop, or `while` loop in the code editor below and run it.
    """)
    display_text(content_text, content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
# Example of an if statement
temperature = 30
if temperature > 25:
    print('It is hot outside.')
else:
    print('The weather is pleasant.')
""")

def functions():
    """Displays the Functions content."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # Functions

        Functions are reusable blocks of code that perform a specific task. They help in organizing code, making it more readable and maintainable.

        ## Defining Functions
        Use the `def` keyword to define a function.
        ```python
        def greet():
            print('Hello!')
        ```

        ## Function Arguments
        Functions can take parameters to accept input.
        ```python
        def greet(name):
            print(f'Hello, {name}!')

        greet('Alice')
        ```

        ## Return Values
        Functions can return values using the `return` statement.
        ```python
        def add(a, b):
            return a + b

        result = add(5, 3)
        print(result)  # Outputs: 8
        ```

        ## Lambda Functions
        Lambda functions are anonymous, short functions defined with the `lambda` keyword.
        ```python
        add = lambda a, b: a + b
        print(add(2, 3))  # Outputs: 5
        ```

        ## Docstrings
        Docstrings are string literals that occur as the first statement in a module, function, class, or method definition. They are used to document the object.
        ```python
        def greet(name):
            '''This function greets the person passed in as a parameter'''
            print(f'Hello, {name}!')

        print(greet.__doc__)
        ```

        ## Recursion
        Recursion occurs when a function calls itself. It's useful for solving problems that can be broken down into smaller, similar problems.
        ```python
        def factorial(n):
            if n == 1:
                return 1
            else:
                return n * factorial(n-1)

        print(factorial(5))  # Outputs: 120
        ```

        ## Using Decorators
        Decorators are a powerful tool to modify the behavior of functions or classes.
        ```python
        def my_decorator(func):
            def wrapper():
                print('Before function')
                func()
                print('After function')
            return wrapper

        @my_decorator
        def say_hello():
            print('Hello!')

        say_hello()
        # Outputs:
        # Before function
        # Hello!
        # After function
        ```

        ## Try It Yourself
        Define your own function, add parameters, return values, or experiment with lambda functions in the code editor below.
    """)
    display_text(content_text, content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
# Define a function to multiply two numbers
def multiply(a, b):
    return a * b

result = multiply(4, 5)
print('Multiplication result:', result)
""")

def modules_packages():
    """Displays the Modules and Packages content."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # Modules and Packages

        Modules are files containing Python code, such as functions and classes. Packages are directories containing multiple modules. They help in organizing and reusing code.

        ## Importing Modules
        Use the `import` statement to include external modules.
        ```python
        import math
        print(math.sqrt(16))  # Outputs: 4.0
        ```

        You can also import specific functions:
        ```python
        from math import pi
        print(pi)  # Outputs: 3.141592653589793
        ```

        ## Exploring the Standard Library
        The Python Standard Library is a collection of modules and packages that come with Python. Commonly used modules include:
        - `math` - Mathematical functions
        - `datetime` - Working with dates and times
        - `os` - Interacting with the operating system
        - `sys` - System-specific parameters and functions
        - `json` - JSON encoding and decoding

        ## Creating Your Own Modules
        You can create your own modules by writing Python code in a `.py` file.
        ```python
        # my_module.py
        def greet(name):
            print(f'Hello, {name}!')

        # To use this module:
        import my_module
        my_module.greet('Alice')
        ```

        ## Using Packages
        Packages allow you to organize related modules into directories. A package must contain an `__init__.py` file.
        ```
        mypackage/
            __init__.py
            module1.py
            module2.py
        ```

        To import a module from a package:
        ```python
        from mypackage import module1
        ```

        ## Try It Yourself
        Import a module from the standard library or create your own module in the code editor below.
    """)
    display_text(content_text, content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
import math

number = 25
sqrt = math.sqrt(number)
print(f'The square root of {number} is {sqrt}')
""")

def oop():
    """Displays the Object-Oriented Programming content."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # Object-Oriented Programming (OOP)

        OOP is a programming paradigm based on the concept of objects, which contain data and methods.

        ## Classes and Objects
        A class is a blueprint for creating objects. An object is an instance of a class.
        ```python
        class Dog:
            def __init__(self, name):
                self.name = name

            def bark(self):
                print('Woof!')

        my_dog = Dog('Rex')
        my_dog.bark()  # Outputs: Woof!
        ```

        ## Attributes and Methods
        - **Attributes**: Variables that belong to an object.
        - **Methods**: Functions that belong to an object.
        ```python
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

            def introduce(self):
                print(f'My name is {self.name} and I am {self.age} years old.')

        person = Person('Alice', 30)
        person.introduce()  # Outputs: My name is Alice and I am 30 years old.
        ```

        ## Inheritance
        Inheritance allows a class to inherit attributes and methods from another class.
        ```python
        class Animal:
            def __init__(self, name):
                self.name = name

            def speak(self):
                pass

        class Cat(Animal):
            def speak(self):
                print('Meow')

        my_cat = Cat('Whiskers')
        my_cat.speak()  # Outputs: Meow
        ```

        ## Encapsulation
        Encapsulation restricts access to certain components of an object. It is achieved by using private attributes and methods.
        ```python
        class BankAccount:
            def __init__(self, balance):
                self.__balance = balance

            def deposit(self, amount):
                self.__balance += amount

            def get_balance(self):
                return self.__balance

        account = BankAccount(100)
        account.deposit(50)
        print(account.get_balance())  # Outputs: 150
        print(account.__balance)  # Raises AttributeError
        ```

        ## Polymorphism
        Polymorphism allows objects of different classes to be treated as objects of a common superclass. It is often implemented via method overriding.
        ```python
        class Bird:
            def fly(self):
                print('Flying')

        class Sparrow(Bird):
            def fly(self):
                print('Sparrow flying')

        class Penguin(Bird):
            def fly(self):
                print('Penguins cannot fly')

        birds = [Sparrow(), Penguin()]
        for bird in birds:
            bird.fly()
        # Outputs:
        # Sparrow flying
        # Penguins cannot fly
        ```

        ## Try It Yourself
        Create your own Tkinter window with different widgets and layout managers in the code editor below.
    """)
    display_text(content_text, content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def drive(self):
        print(f'{self.brand} is driving.')

class Car(Vehicle):
    def drive(self):
        print(f'{self.brand} car is driving.')

my_car = Car('Toyota')
my_car.drive()  # Outputs: Toyota car is driving.
""")

def file_handling():
    """Displays the File Handling content."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # File Handling

        Python provides built-in functions to work with files.

        ## Opening and Closing Files
        Use the `open()` function to open a file.
        ```python
        file = open('example.txt', 'r')  # 'r' for reading
        file.close()
        ```

        ## Reading Files
        You can read the entire content using `read()`, `readlines()`, or iterate over the file.
        ```python
        with open('example.txt', 'r') as file:
            content = file.read()
            print(content)
        ```

        ## Writing Files
        Use `write()` or `writelines()` to write to a file.
        ```python
        with open('example.txt', 'w') as file:
            file.write('Hello, World!')
        ```

        ## Working with File Paths
        Use the `os` and `pathlib` modules to work with file paths.
        ```python
        import os
        path = os.path.join('folder', 'file.txt')

        from pathlib import Path
        path = Path('folder') / 'file.txt'
        ```

        ## Try It Yourself
        Perform file operations like reading, writing, and working with file paths in the code editor below.
        **Note:** File operations may not work as expected in some environments.
    """)
    display_text(content_text, content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
import os

# Writing to a file
with open('test.txt', 'w') as file:
    file.write('This is a test file.')

# Reading from the file
with open('test.txt', 'r') as file:
    content = file.read()
    print(content)
""")

def exception_handling():
    """Displays the Exception Handling content."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # Exception Handling

        Exception handling allows you to handle errors gracefully.

        ## try and except
        Use `try` and `except` blocks to handle exceptions.
        ```python
        try:
            x = 1 / 0
        except ZeroDivisionError:
            print('Cannot divide by zero')
        ```

        ## else and finally
        You can use `else` and `finally` blocks with `try-except`.
        ```python
        try:
            x = 5
        except ZeroDivisionError:
            print('Error')
        else:
            print('No errors')
        finally:
            print('Execution complete')
        ```

        ## Raising Exceptions
        Use the `raise` statement to trigger exceptions.
        ```python
        def divide(a, b):
            if b == 0:
                raise ValueError('Cannot divide by zero')
            return a / b
        ```

        ## Custom Exceptions
        Define your own exception classes by inheriting from `Exception`.
        ```python
        class MyError(Exception):
            pass

        def do_something():
            raise MyError('Something went wrong')
        ```

        ## Try It Yourself
        Implement `try-except` blocks, raise exceptions, or create custom exceptions in the code editor below.
    """)
    display_text(content_text, content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
try:
    number = int(input('Enter a number: '))
    print('You entered:', number)
except ValueError:
    print('That is not a valid number!')
finally:
    print('Execution complete.')
""")

def advanced_topics():
    """Displays the Advanced Topics content."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # Advanced Topics

        Explore advanced Python concepts to deepen your understanding.

        ## List Comprehensions
        List comprehensions provide a concise way to create lists.
        ```python
        squares = [x**2 for x in range(10)]
        ```

        ## Generators and Iterators
        Generators are functions that return an iterator using the `yield` statement.
        ```python
        def count_up_to(n):
            count = 1
            while count <= n:
                yield count
                count += 1

        for number in count_up_to(5):
            print(number)
        # Outputs: 1 2 3 4 5
        ```

        ## Decorators
        Decorators are functions that modify the behavior of other functions.
        ```python
        def my_decorator(func):
            def wrapper():
                print('Before function')
                func()
                print('After function')
            return wrapper

        @my_decorator
        def say_hello():
            print('Hello!')

        say_hello()
        # Outputs:
        # Before function
        # Hello!
        # After function
        ```

        ## Context Managers
        Context managers allow you to allocate and release resources precisely when you want. They are commonly used with the `with` statement.
        ```python
        with open('file.txt', 'w') as file:
            file.write('Hello, World!')
        ```

        ## Multithreading and Multiprocessing
        - **Multithreading**: Concurrent execution of threads within a process.
        - **Multiprocessing**: Concurrent execution of multiple processes.

        ### Example with threading:
        ```python
        import threading

        def print_numbers():
            for i in range(5):
                print(i)

        thread = threading.Thread(target=print_numbers)
        thread.start()
        ```

        ## Networking
        Python provides libraries for networking tasks, such as socket programming and HTTP requests.

        ### Example with `requests`:
        ```python
        import requests

        response = requests.get('https://api.github.com')
        print(response.status_code)
        ```

        ## Testing and Debugging
        Python offers tools for testing and debugging, such as `unittest` and `pdb`.

        ### Example with `unittest`:
        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_addition(self):
                self.assertEqual(1 + 1, 2)

        if __name__ == '__main__':
            unittest.main()
        ```

        ## Try It Yourself
        Experiment with advanced topics like list comprehensions, generators, decorators, and more in the code editor below.
    """)
    display_text(content_text, content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
# List comprehension example
even_numbers = [x for x in range(20) if x % 2 == 0]
print('Even numbers:', even_numbers)

# Generator example
def fibonacci(n):
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
""")

def quizzes():
    """Opens the Quiz selection window."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # Quizzes and Assessments

        Test your knowledge with the following quizzes.

        ## Select a Quiz
        Choose a topic to start the quiz:
    """)
    display_text(content_text, content)
    quiz_window()

def quiz_window():
    """Creates a new window for selecting quizzes."""
    quiz_win = tk.Toplevel(root)
    quiz_win.title("Quizzes")

    quiz_frame = tk.Frame(quiz_win, padx=10, pady=10, bg=current_theme["bg"])
    quiz_frame.pack(fill=tk.BOTH, expand=True)

    quiz_topics = [
        "Variables and Data Types",
        "Control Structures",
        "Functions",
        "Modules and Packages",
        "Object-Oriented Programming",
        "File Handling",
        "Exception Handling",
        "List Comprehensions",
        "Generators and Iterators",
        "Decorators"
    ]

    tk.Label(
        quiz_frame, text="Select a Quiz Topic:",
        font=('Arial', 14), bg=current_theme["bg"], fg=current_theme["fg"]
    ).pack(pady=10)

    for topic in quiz_topics:
        btn = tk.Button(
            quiz_frame, text=topic, width=30,
            command=lambda t=topic: start_quiz(t, quiz_win),
            font=('Arial', 12), bg=current_theme["button_bg"],
            fg=current_theme["button_fg"]
        )
        btn.pack(pady=5)

def start_quiz(topic, parent_window):
    """Starts the selected quiz."""
    parent_window.destroy()
    clear_text(content_text)
    topic_quizzes = {
        "Variables and Data Types": quiz_variables,
        "Control Structures": quiz_control_structures,
        "Functions": quiz_functions,
        "Modules and Packages": quiz_modules_packages,
        "Object-Oriented Programming": quiz_oop,
        "File Handling": quiz_file_handling,
        "Exception Handling": quiz_exception_handling,
        "List Comprehensions": quiz_list_comprehensions,
        "Generators and Iterators": quiz_generators_iterators,
        "Decorators": quiz_decorators
    }
    quiz_func = topic_quizzes.get(topic, placeholder_quiz)
    quiz_func()

def placeholder_quiz():
    """Displays a placeholder for quizzes."""
    clear_text(content_text)
    content = textwrap.dedent("""
        # Quiz Coming Soon!

        This quiz is under development. Stay tuned for more content.
    """)
    display_text(content_text, content)

# ---------------- Quiz Functions ----------------

def run_quiz(questions):
    """Runs the quiz with the provided questions."""
    quiz_win = tk.Toplevel(root)
    quiz_win.title("Quiz")

    quiz_frame = tk.Frame(quiz_win, padx=10, pady=10, bg=current_theme["bg"])
    quiz_frame.pack(fill=tk.BOTH, expand=True)

    current_question = [0]
    score = [0]

    question_label = tk.Label(
        quiz_frame, text="", wraplength=800,
        font=('Arial', 12), justify='left',
        bg=current_theme["bg"], fg=current_theme["fg"]
    )
    question_label.pack(pady=10)
    quiz_widgets.append(question_label)

    var = tk.StringVar()
    option_buttons = []
    for _ in range(4):
        rb = tk.Radiobutton(
            quiz_frame, text="", variable=var, value="",
            wraplength=800, anchor='w', justify='left',
            font=('Arial', 12), bg=current_theme["bg"],
            fg=current_theme["fg"]
        )
        rb.pack(anchor='w', pady=2)
        option_buttons.append(rb)
        quiz_widgets.append(rb)

    submit_btn = tk.Button(
        quiz_frame, text="Submit",
        command=lambda: submit_answer(),
        font=('Arial', 12),
        bg=current_theme["button_bg"], fg=current_theme["button_fg"]
    )
    submit_btn.pack(pady=10)
    quiz_widgets.append(submit_btn)

    feedback_label = tk.Label(
        quiz_frame, text="",
        font=('Arial', 12), bg=current_theme["bg"],
        fg=current_theme["fg"]
    )
    feedback_label.pack()
    quiz_widgets.append(feedback_label)

    def display_question():
        """Displays the current question and options."""
        if current_question[0] < len(questions):
            q = questions[current_question[0]]
            question_label.config(text=f"Q{current_question[0] +1}: {q['question']}")
            var.set(None)
            for idx, option in enumerate(q['options']):
                option_buttons[idx].config(text=option, value=option)
        else:
            end_quiz()

    def submit_answer():
        """Handles the submission of an answer."""
        selected = var.get()
        if not selected:
            show_error("Please select an option before submitting.")
            return
        correct = questions[current_question[0]]['answer']
        if selected == correct:
            score[0] += 1
            feedback_label.config(text="Correct!", fg='green')
        else:
            feedback_label.config(text=f"Incorrect! The correct answer is: {correct}", fg='red')
        current_question[0] += 1
        if current_question[0] < len(questions):
            quiz_frame.after(1500, display_question)
        else:
            quiz_frame.after(1500, end_quiz)

    def end_quiz():
        """Ends the quiz and displays the score."""
        feedback_label.config(
            text=f"Quiz Completed! Your score: {score[0]}/{len(questions)}",
            fg='blue'
        )
        submit_btn.config(state=tk.DISABLED)

    display_question()

def quiz_variables():
    """Quiz for Variables and Data Types."""
    questions = [
        {
            "question": "What is the correct way to create a variable with the integer value 5?",
            "options": ["x = 5", "x == 5", "x: int = 5", "int x = 5"],
            "answer": "x = 5"
        },
        {
            "question": "Which data type is mutable?",
            "options": ["Tuple", "List", "String", "Integer"],
            "answer": "List"
        },
        {
            "question": "How do you convert a string '123' to an integer?",
            "options": ["int('123')", "str(123)", "float('123')", "None of the above"],
            "answer": "int('123')"
        }
    ]
    run_quiz(questions)

def quiz_control_structures():
    """Quiz for Control Structures."""
    questions = [
        {
            "question": "Which keyword is used to start a loop that iterates over a sequence?",
            "options": ["loop", "for", "while", "iterate"],
            "answer": "for"
        },
        {
            "question": "What does the `break` statement do?",
            "options": ["Exits the current loop", "Skips to the next iteration", "Terminates the program", "None of the above"],
            "answer": "Exits the current loop"
        },
        {
            "question": "Which of the following is a correct `if` statement?",
            "options": [
                "if x = 5:",
                "if (x == 5)",
                "if x == 5:",
                "if x === 5:"
            ],
            "answer": "if x == 5:"
        }
    ]
    run_quiz(questions)

def quiz_functions():
    """Quiz for Functions."""
    questions = [
        {
            "question": "How do you define a function in Python?",
            "options": ["function myFunc():", "def myFunc():", "define myFunc():", "func myFunc():"],
            "answer": "def myFunc():"
        },
        {
            "question": "What keyword is used to return a value from a function?",
            "options": ["send", "give", "return", "output"],
            "answer": "return"
        },
        {
            "question": "What is a lambda function?",
            "options": [
                "A named function",
                "An anonymous, short function",
                "A function that returns multiple values",
                "None of the above"
            ],
            "answer": "An anonymous, short function"
        }
    ]
    run_quiz(questions)

def quiz_modules_packages():
    """Quiz for Modules and Packages."""
    questions = [
        {
            "question": "How do you import the `math` module?",
            "options": ["import math", "include math", "using math", "from math import *"],
            "answer": "import math"
        },
        {
            "question": "What file must be present in a directory to make it a Python package?",
            "options": ["__init__.py", "package.py", "module.py", "main.py"],
            "answer": "__init__.py"
        },
        {
            "question": "How do you import only the `sqrt` function from the `math` module?",
            "options": [
                "import math.sqrt",
                "from math import sqrt",
                "import sqrt from math",
                "from sqrt import math"
            ],
            "answer": "from math import sqrt"
        }
    ]
    run_quiz(questions)

def quiz_oop():
    """Quiz for Object-Oriented Programming."""
    questions = [
        {
            "question": "What is an object in OOP?",
            "options": [
                "A blueprint for creating classes",
                "An instance of a class",
                "A function within a class",
                "None of the above"
            ],
            "answer": "An instance of a class"
        },
        {
            "question": "What keyword is used to inherit from a superclass?",
            "options": ["inherits", "extends", "super", "class SubClass(SuperClass):"],
            "answer": "class SubClass(SuperClass):"
        },
        {
            "question": "What is encapsulation?",
            "options": [
                "Allowing access to internal object data",
                "Restricting access to internal object data",
                "Inheriting attributes and methods",
                "None of the above"
            ],
            "answer": "Restricting access to internal object data"
        }
    ]
    run_quiz(questions)

def quiz_file_handling():
    """Quiz for File Handling."""
    questions = [
        {
            "question": "Which mode is used to append to a file?",
            "options": ["'r'", "'w'", "'a'", "'x'"],
            "answer": "'a'"
        },
        {
            "question": "What does the `read()` method do?",
            "options": [
                "Writes data to a file",
                "Reads the entire content of a file",
                "Closes the file",
                "Deletes the file"
            ],
            "answer": "Reads the entire content of a file"
        },
        {
            "question": "Which module is used to work with file paths?",
            "options": ["os", "sys", "pathlib", "All of the above"],
            "answer": "All of the above"
        }
    ]
    run_quiz(questions)

def quiz_exception_handling():
    """Quiz for Exception Handling."""
    questions = [
        {
            "question": "Which keyword is used to handle exceptions?",
            "options": ["try", "catch", "except", "finally"],
            "answer": "except"
        },
        {
            "question": "What does the `finally` block do?",
            "options": [
                "Executes only if an exception occurs",
                "Executes only if no exception occurs",
                "Executes regardless of whether an exception occurs",
                "None of the above"
            ],
            "answer": "Executes regardless of whether an exception occurs"
        },
        {
            "question": "How do you raise an exception?",
            "options": ["raise Exception('Error')", "throw Exception('Error')", "emit Exception('Error')", "None of the above"],
            "answer": "raise Exception('Error')"
        }
    ]
    run_quiz(questions)

def quiz_list_comprehensions():
    """Quiz for List Comprehensions."""
    questions = [
        {
            "question": "What does the following list comprehension do? `[x*2 for x in range(5)]`",
            "options": [
                "Creates a list of even numbers",
                "Creates a list of numbers from 0 to 4",
                "Creates a list of numbers from 0 to 8 in steps of 2",
                "None of the above"
            ],
            "answer": "Creates a list of even numbers"
        },
        {
            "question": "How do you include a condition in a list comprehension?",
            "options": [
                "After the expression, using `if`",
                "Before the expression, using `if`",
                "Using `filter()`",
                "Conditions are not allowed"
            ],
            "answer": "After the expression, using `if`"
        },
        {
            "question": "What is the output of `[x for x in range(3)]`?",
            "options": [
                "[0, 1, 2]",
                "[1, 2, 3]",
                "[0, 1, 2, 3]",
                "None of the above"
            ],
            "answer": "[0, 1, 2]"
        }
    ]
    run_quiz(questions)

def quiz_generators_iterators():
    """Quiz for Generators and Iterators."""
    questions = [
        {
            "question": "What keyword is used to define a generator function?",
            "options": ["yield", "return", "generator", "gen"],
            "answer": "yield"
        },
        {
            "question": "What does the `next()` function do with a generator?",
            "options": [
                "Starts the generator",
                "Retrieves the next value",
                "Closes the generator",
                "None of the above"
            ],
            "answer": "Retrieves the next value"
        },
        {
            "question": "Which of the following is an iterator?",
            "options": ["List", "Generator", "Dictionary", "All of the above"],
            "answer": "Generator"
        }
    ]
    run_quiz(questions)

def quiz_decorators():
    """Quiz for Decorators."""
    questions = [
        {
            "question": "What is a decorator in Python?",
            "options": [
                "A function that modifies another function",
                "A function that adds arguments to another function",
                "A class that inherits from another class",
                "None of the above"
            ],
            "answer": "A function that modifies another function"
        },
        {
            "question": "How do you apply a decorator to a function?",
            "options": [
                "By calling the decorator and passing the function",
                "Using the `@` symbol above the function definition",
                "Both A and B",
                "None of the above"
            ],
            "answer": "Both A and B"
        },
        {
            "question": "What does the following decorator do?\n```python\ndef my_decorator(func):\n    def wrapper():\n        print('Before')\n        func()\n        print('After')\n    return wrapper\n```",
            "options": [
                "Prints 'Before' and 'After' when the function is called",
                "Adds arguments to the function",
                "None of the above",
                "Both A and B"
            ],
            "answer": "Prints 'Before' and 'After' when the function is called"
        }
    ]
    run_quiz(questions)

# ---------------- Module-Specific Content Functions ----------------

def random_module():
    """Displays the Random Module content."""
    clear_text(content_text)
    random_content = textwrap.dedent("""
        # Random Module

        The `random` module in Python provides functions for generating random numbers and performing random operations.

        ## Importing the `random` Module
        ```python
        import random
        ```

        ## Generating Random Numbers
        - **`random.randint(a, b)`**: Returns a random integer N such that `a <= N <= b`.
        - **`random.randrange(start, stop, step)`**: Returns a randomly selected element from `range(start, stop, step)`.
        - **`random.uniform(a, b)`**: Returns a random floating-point number N such that `a <= N <= b`.

        ```python
        random_int = random.randint(1, 10)
        print(f'Random Integer between 1 and 10: {random_int}')

        random_float = random.uniform(1.0, 10.0)
        print(f'Random Float between 1.0 and 10.0: {random_float}')
        ```

        ## Choosing Random Elements
        - **`random.choice(sequence)`**: Returns a randomly selected element from a non-empty sequence.
        - **`random.choices(population, weights=None, *, cum_weights=None, k=1)`**: Returns a list of `k` elements chosen from `population` with replacement.
        - **`random.sample(population, k)`**: Returns a list of `k` unique elements chosen from `population`.

        ```python
        fruits = ['apple', 'banana', 'cherry', 'date']
        selected_fruit = random.choice(fruits)
        print(f'Selected Fruit: {selected_fruit}')

        multiple_fruits = random.choices(fruits, k=2)
        print(f'Multiple Fruits: {multiple_fruits}')

        unique_fruits = random.sample(fruits, 2)
        print(f'Unique Fruits: {unique_fruits}')
        ```

        ## Shuffling a List
        - **`random.shuffle(x)`**: Shuffles the sequence `x` in place.

        ```python
        numbers = [1, 2, 3, 4, 5]
        random.shuffle(numbers)
        print(f'Shuffled Numbers: {numbers}')
        ```

        ## Setting a Seed
        - **`random.seed(a=None)`**: Initializes the random number generator. If `a` is omitted or `None`, the current system time is used.

        ```python
        random.seed(42)
        print(random.randint(1, 100))  # Output will be the same every time with the same seed
        ```

        ## Try It Yourself
        Experiment with the `random` module in the code editor below. Try generating random numbers, selecting random elements from a list, shuffling lists, and setting seeds.
    """)
    display_text(content_text, random_content)
    code_entry.delete('1.0', tk.END)
    sample_code = textwrap.dedent("""
import random

# Generate a random integer between 1 and 100
rand_int = random.randint(1, 100)
print(f'Random Integer: {rand_int}')

# Generate a random float between 0 and 1
rand_float = random.random()
print(f'Random Float: {rand_float}')

# Choose a random element from a list
colors = ['red', 'green', 'blue', 'yellow']
selected_color = random.choice(colors)
print(f'Selected Color: {selected_color}')

# Shuffle a list
deck = ['Ace', 'King', 'Queen', 'Jack', '10']
random.shuffle(deck)
print(f'Shuffled Deck: {deck}')

# Set a seed and generate a random number
random.seed(123)
seeded_rand = random.randint(1, 100)
print(f'Seeded Random Integer: {seeded_rand}')
""")
    code_entry.insert(tk.END, sample_code)

def time_module():
    """Displays the Time Module content."""
    clear_text(content_text)
    time_content = textwrap.dedent("""
        # Time Module

        The `time` module in Python provides various time-related functions that allow you to work with time-related tasks, such as measuring execution time, creating delays, and formatting time.

        ## Importing the `time` Module
        ```python
        import time
        ```

        ## Current Time
        - **`time.time()`**: Returns the current time in seconds since the Epoch.
        - **`time.ctime([secs])`**: Converts a time expressed in seconds since the Epoch to a string.
        - **`time.localtime([secs])`**: Converts a time expressed in seconds since the Epoch to a `struct_time` in local time.

        ```python
        current_time = time.time()
        print(f'Current Time (Epoch): {current_time}')

        readable_time = time.ctime(current_time)
        print(f'Readable Time: {readable_time}')

        local_time = time.localtime(current_time)
        print(f'Local Time: {local_time}')
        ```

        ## Sleep
        - **`time.sleep(seconds)`**: Suspends execution for the given number of seconds.

        ```python
        print('Sleeping for 2 seconds...')
        time.sleep(2)
        print('Awake!')
        ```

        ## Measuring Execution Time
        Use `time.perf_counter()` to measure the execution time of code snippets accurately.
        ```python
        start = time.perf_counter()
        # Code to measure
        time.sleep(1)
        end = time.perf_counter()
        print(f'Execution Time: {end - start} seconds')
        ```

        ## Formatting Time
        Use `time.strftime()` to format `struct_time` into readable strings.
        ```python
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(f'Formatted Time: {formatted_time}')
        ```

        ## Using `time.strptime()`
        Parse a string representing a time according to a format.
        ```python
        time_str = '2024-04-27 15:30:00'
        parsed_time = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        print(f'Parsed Time: {parsed_time}')
        ```

        ## Try It Yourself
        Experiment with the `time` module in the code editor below. Try getting the current time, making the program sleep, measuring execution time, and formatting time strings.
    """)
    display_text(content_text, time_content)
    code_entry.delete('1.0', tk.END)
    sample_code = textwrap.dedent("""
import time

# Get current time in Epoch
current_time = time.time()
print(f'Current Time (Epoch): {current_time}')

# Convert to readable time
readable_time = time.ctime(current_time)
print(f'Readable Time: {readable_time}')

# Local time struct
local_time = time.localtime(current_time)
print(f'Local Time: {local_time}')

# Sleep for 2 seconds
print('Sleeping for 2 seconds...')
time.sleep(2)
print('Awake!')

# Measure execution time
start = time.perf_counter()
# Simulate a task
time.sleep(1)
end = time.perf_counter()
print(f'Execution Time: {end - start} seconds')

# Format time
formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print(f'Formatted Time: {formatted_time}')

# Parse time string
time_str = '2024-04-27 15:30:00'
parsed_time = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
print(f'Parsed Time: {parsed_time}')
""")
    code_entry.insert(tk.END, sample_code)

def os_module():
    """Displays the OS Module content."""
    clear_text(content_text)
    os_content = textwrap.dedent("""
        # OS Module

        The `os` module provides a way of using operating system-dependent functionality.

        ## Importing the `os` Module
        ```python
        import os
        ```

        ## Working with Directories
        - **`os.getcwd()`**: Returns the current working directory.
        - **`os.listdir(path='.')`**: Returns a list of entries in the given directory.
        - **`os.mkdir(path)`**: Creates a new directory.
        - **`os.chdir(path)`**: Changes the current working directory.
        - **`os.rmdir(path)`**: Removes a directory.

        ```python
        current_dir = os.getcwd()
        print(f'Current Directory: {current_dir}')

        directories = os.listdir('.')
        print(f'Directories and Files: {directories}')

        # Create a new directory
        os.mkdir('new_folder')
        print('Created new_folder')

        # Change directory
        os.chdir('new_folder')
        print(f'Changed Directory to: {os.getcwd()}')

        # Remove directory
        os.chdir('..')
        os.rmdir('new_folder')
        print('Removed new_folder')
        ```

        ## Environment Variables
        - **`os.environ`**: A mapping object representing the string environment.
        - **`os.getenv(key, default=None)`**: Returns the value of the environment variable `key` if it exists, else `default`.
        - **`os.putenv(key, value)`**: Sets the environment variable `key` to the value `value`.

        ```python
        home_dir = os.getenv('HOME', 'Not Found')
        print(f'Home Directory: {home_dir}')

        os.putenv('MY_VAR', '12345')
        print(f"MY_VAR: {os.getenv('MY_VAR')}")
        ```

        ## Path Manipulations
        Use `os.path` for common path operations.
        ```python
        path = os.path.join('folder', 'file.txt')
        print(f'Joined Path: {path}')

        is_file = os.path.isfile(path)
        print(f'Is File: {is_file}')

        is_dir = os.path.isdir('folder')
        print(f'Is Directory: {is_dir}')
        ```

        ## Try It Yourself
        Experiment with the `os` module in the code editor below. Try navigating directories, creating/removing folders, and manipulating environment variables.
    """)
    display_text(content_text, os_content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
import os

# Get current directory
current_dir = os.getcwd()
print(f'Current Directory: {current_dir}')

# List directories and files
directories = os.listdir('.')
print(f'Directories and Files: {directories}')

# Create a new directory
os.mkdir('test_folder')
print('Created test_folder')

# Change directory
os.chdir('test_folder')
print(f'Changed Directory to: {os.getcwd()}')

# Remove directory
os.chdir('..')
os.rmdir('test_folder')
print('Removed test_folder')
""")

def tkinter_module():
    """Displays the Tkinter Module content."""
    clear_text(content_text)
    tkinter_content = textwrap.dedent("""
        # Tkinter Module

        Tkinter is Python's de-facto standard GUI (Graphical User Interface) package. It provides a fast and easy way to create GUI applications.

        ## Importing Tkinter
        ```python
        import tkinter as tk
        from tkinter import messagebox
        ```

        ## Creating a Simple Window
        ```python
        root = tk.Tk()
        root.title("Simple Tkinter Window")
        root.geometry("300x200")

        label = tk.Label(root, text="Hello, Tkinter!", font=('Arial', 14))
        label.pack(pady=20)

        button = tk.Button(root, text="Click Me", command=lambda: messagebox.showinfo("Info", "Button Clicked"))
        button.pack(pady=10)

        root.mainloop()
        ```

        ## Widgets
        - **Label**: Displays text or images.
        - **Button**: Triggers actions when clicked.
        - **Entry**: Single-line text input.
        - **Text**: Multi-line text input.
        - **Canvas**: Drawing area.
        - **Frame**: Container for other widgets.

        ## Layout Managers
        - **Pack**: Packs widgets relative to each other.
        - **Grid**: Places widgets in a grid.
        - **Place**: Places widgets at absolute positions.

        ## Example with Grid Layout
        ```python
        root = tk.Tk()
        root.title("Grid Layout Example")
        root.geometry("400x300")

        tk.Label(root, text="First Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Last Name:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root).grid(row=1, column=1, padx=10, pady=10)

        def submit():
            first = first_name.get()
            last = last_name.get()
            messagebox.showinfo("Info", f"Hello, {first} {last}!")

        first_name = tk.Entry(root)
        first_name.grid(row=0, column=1, padx=10, pady=10)

        last_name = tk.Entry(root)
        last_name.grid(row=1, column=1, padx=10, pady=10)

        submit_button = tk.Button(root, text="Submit", command=submit)
        submit_button.grid(row=2, column=0, columnspan=2, pady=20)

        root.mainloop()
        ```

        ## Try It Yourself
        Create your own Tkinter window with different widgets and layout managers in the code editor below.
    """)
    display_text(content_text, tkinter_content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
import tkinter as tk
from tkinter import messagebox

def greet():
    name = name_entry.get()
    messagebox.showinfo("Greeting", f"Hello, {name}!")

root = tk.Tk()
root.title("Greeting App")
root.geometry("350x200")

tk.Label(root, text="Enter Your Name:", font=('Arial', 12)).pack(pady=10)
name_entry = tk.Entry(root, font=('Arial', 12))
name_entry.pack(pady=5)

greet_button = tk.Button(root, text="Greet", command=greet, bg=current_theme["button_bg"], fg=current_theme["button_fg"], font=('Arial', 12))
greet_button.pack(pady=20)

root.mainloop()
""")

def pyautogui_module():
    """Displays the PyAutoGUI Module content."""
    if pyautogui is None:
        clear_text(content_text)
        pyautogui_content = textwrap.dedent("""
            # PyAutoGUI Module

            PyAutoGUI is a cross-platform GUI automation Python module for human beings. Used to programmatically control the mouse and keyboard.

            ## Installation
            ```bash
            pip install pyautogui
            ```

            ## Importing PyAutoGUI
            ```python
            import pyautogui
            ```

            ## Moving the Mouse
            ```python
            pyautogui.moveTo(100, 150, duration=1)  # Move to (100, 150) over 1 second
            pyautogui.moveRel(0, 50, duration=0.5)   # Move relative by (0, 50)
            ```

            ## Clicking
            ```python
            pyautogui.click()           # Left click at current position
            pyautogui.click(200, 200)   # Left click at (200, 200)
            pyautogui.rightClick()      # Right click
            pyautogui.doubleClick()     # Double click
            ```

            ## Keyboard Automation
            ```python
            pyautogui.write('Hello, World!', interval=0.1)  # Type with a 0.1s delay between each key
            pyautogui.press('enter')                         # Press the Enter key
            pyautogui.hotkey('ctrl', 'c')                    # Press Ctrl+C
            ```

            ## Taking Screenshots
            ```python
            screenshot = pyautogui.screenshot()
            screenshot.save('screenshot.png')  # Save the screenshot
            ```

            ## Locating on Screen
            ```python
            button_location = pyautogui.locateOnScreen('button.png')
            if button_location:
                pyautogui.click(button_location)
            else:
                print("Button not found on screen.")
            ```

            ## Try It Yourself
            Use the `pyautogui` module in the code editor below to automate mouse movements, clicks, and keyboard inputs. **Be cautious** when running automation scripts to avoid unintended actions.
        """)
        display_text(content_text, pyautogui_content)
        code_entry.delete('1.0', tk.END)
        code_entry.insert(tk.END, """
import pyautogui
import time

# Move the mouse to (500, 500) over 2 seconds
pyautogui.moveTo(500, 500, duration=2)

# Click at the current mouse position
pyautogui.click()

# Type 'Automated typing...' with a 0.1s interval between each character
pyautogui.write('Automated typing...', interval=0.1)

# Press the Enter key
pyautogui.press('enter')

# Take a screenshot and save it
screenshot = pyautogui.screenshot()
screenshot.save('automation_screenshot.png')

# Pause for 5 seconds
time.sleep(5)

# Move relative by (100, 0) and double click
pyautogui.moveRel(100, 0, duration=1)
pyautogui.doubleClick()
""")
    else:
        # If PyAutoGUI is installed, provide content
        clear_text(content_text)
        pyautogui_content = textwrap.dedent("""
            # PyAutoGUI Module

            PyAutoGUI is a cross-platform GUI automation Python module for human beings. Used to programmatically control the mouse and keyboard.

            ## Importing PyAutoGUI
            ```python
            import pyautogui
            ```

            ## Moving the Mouse
            ```python
            pyautogui.moveTo(100, 150, duration=1)  # Move to (100, 150) over 1 second
            pyautogui.moveRel(0, 50, duration=0.5)   # Move relative by (0, 50)
            ```

            ## Clicking
            ```python
            pyautogui.click()           # Left click at current position
            pyautogui.click(200, 200)   # Left click at (200, 200)
            pyautogui.rightClick()      # Right click
            pyautogui.doubleClick()     # Double click
            ```

            ## Keyboard Automation
            ```python
            pyautogui.write('Hello, World!', interval=0.1)  # Type with a 0.1s delay between each key
            pyautogui.press('enter')                         # Press the Enter key
            pyautogui.hotkey('ctrl', 'c')                    # Press Ctrl+C
            ```

            ## Taking Screenshots
            ```python
            screenshot = pyautogui.screenshot()
            screenshot.save('screenshot.png')  # Save the screenshot
            ```

            ## Locating on Screen
            ```python
            button_location = pyautogui.locateOnScreen('button.png')
            if button_location:
                pyautogui.click(button_location)
            else:
                print("Button not found on screen.")
            ```

            ## Try It Yourself
            Use the `pyautogui` module in the code editor below to automate mouse movements, clicks, and keyboard inputs. **Be cautious** when running automation scripts to avoid unintended actions.
        """)
        display_text(content_text, pyautogui_content)
        code_entry.delete('1.0', tk.END)
        code_entry.insert(tk.END, """
import pyautogui
import time

# Move the mouse to (500, 500) over 2 seconds
pyautogui.moveTo(500, 500, duration=2)

# Click at the current mouse position
pyautogui.click()

# Type 'Automated typing...' with a 0.1s interval between each character
pyautogui.write('Automated typing...', interval=0.1)

# Press the Enter key
pyautogui.press('enter')

# Take a screenshot and save it
screenshot = pyautogui.screenshot()
screenshot.save('automation_screenshot.png')

# Pause for 5 seconds
time.sleep(5)

# Move relative by (100, 0) and double click
pyautogui.moveRel(100, 0, duration=1)
pyautogui.doubleClick()
""")

def discord_module():
    """Displays the Discord Module content."""
    if discord is None:
        clear_text(content_text)
        discord_content = textwrap.dedent("""
            # Discord Module

            The `discord.py` library allows you to interact with the Discord API to create bots that can perform automated tasks, respond to messages, and much more.

            ## Installation
            ```bash
            pip install discord.py
            ```

            ## Creating a Discord Bot
            1. **Create a Discord Application:**
               - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
               - Click "New Application" and provide a name.

            2. **Add a Bot to the Application:**
               - Navigate to the "Bot" tab.
               - Click "Add Bot" and confirm.

            3. **Copy the Bot Token:**
               - Under the Bot section, click "Copy" to copy your bot's token. **Keep this token secret!**

            4. **Invite the Bot to Your Server:**
               - Go to the "OAuth2" tab.
               - Under "Scopes," select `bot`.
               - Under "Bot Permissions," select the permissions your bot needs.
               - Copy the generated URL and paste it into your browser to invite the bot to your server.

            ## Writing a Simple Discord Bot
            ```python
            import discord
            from discord.ext import commands

            # Replace 'YOUR_BOT_TOKEN' with your actual bot token
            TOKEN = 'YOUR_BOT_TOKEN'

            bot = commands.Bot(command_prefix='!')

            @bot.event
            async def on_ready():
                print(f'Logged in as {bot.user.name}')

            @bot.command()
            async def hello(ctx):
                await ctx.send('Hello! I am your bot.')

            bot.run(TOKEN)
            ```

            ## Running the Bot
            - Save the above code in a file, e.g., `discord_bot.py`.
            - Replace `'YOUR_BOT_TOKEN'` with the actual token.
            - Run the script:
              ```bash
              python discord_bot.py
              ```
            - In your Discord server, type `!hello` and the bot should respond.

            ## Try It Yourself
            Create and run your own Discord bot using the code editor below. **Ensure you keep your bot token secure** and never share it publicly.
        """)
        display_text(content_text, discord_content)
        code_entry.delete('1.0', tk.END)
        code_entry.insert(tk.END, """
import discord
from discord.ext import commands

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'YOUR_BOT_TOKEN'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

bot.run(TOKEN)
""")
    else:
        # If Discord.py is installed, provide content
        clear_text(content_text)
        discord_content = textwrap.dedent("""
            # Discord Module

            The `discord.py` library allows you to interact with the Discord API to create bots that can perform automated tasks, respond to messages, and much more.

            ## Importing Discord.py
            ```python
            import discord
            from discord.ext import commands
            ```

            ## Writing a Simple Discord Bot
            ```python
            import discord
            from discord.ext import commands

            # Replace 'YOUR_BOT_TOKEN' with your actual bot token
            TOKEN = 'YOUR_BOT_TOKEN'

            bot = commands.Bot(command_prefix='!')

            @bot.event
            async def on_ready():
                print(f'Logged in as {bot.user.name}')

            @bot.command()
            async def hello(ctx):
                await ctx.send('Hello! I am your bot.')

            bot.run(TOKEN)
            ```

            ## Running the Bot
            - Save the above code in a file, e.g., `discord_bot.py`.
            - Replace `'YOUR_BOT_TOKEN'` with the actual token.
            - Run the script:
              ```bash
              python discord_bot.py
              ```
            - In your Discord server, type `!hello` and the bot should respond.

            ## Advanced Commands
            You can create more complex commands, handle events, and add functionalities like moderation, music playback, etc.
            ```python
            @bot.command()
            async def add(ctx, a: int, b: int):
                await ctx.send(f'The sum of {a} and {b} is {a + b}')
            ```

            ## Try It Yourself
            Create and run your own Discord bot using the code editor below. **Ensure you keep your bot token secure** and never share it publicly.
        """)
        display_text(content_text, discord_content)
        code_entry.delete('1.0', tk.END)
        code_entry.insert(tk.END, """
import discord
from discord.ext import commands

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'YOUR_BOT_TOKEN'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def greet(ctx, name: str):
    await ctx.send(f'Hello, {name}!')

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(f'The sum of {a} and {b} is {a + b}')

bot.run(TOKEN)
""")

def requests_module():
    """Displays the Requests Module content."""
    clear_text(content_text)
    requests_content = textwrap.dedent("""
        # Requests Module

        The `requests` module in Python allows you to send HTTP requests easily. 
        It's a powerful tool for interacting with web services, APIs, and scraping web pages.

        ## Importing Requests
        ```python
        import requests
        ```

        ## Making a GET Request
        ```python
        response = requests.get('https://api.github.com')
        print(response.status_code)  # Status Code
        print(response.text)         # Response Body
        ```

        ## Making a POST Request
        ```python
        payload = {'key1': 'value1', 'key2': 'value2'}
        response = requests.post('https://httpbin.org/post', data=payload)
        print(response.text)
        ```

        ## Handling JSON Data
        ```python
        response = requests.get('https://api.github.com')
        data = response.json()
        print(data['current_user_url'])
        ```

        ## Error Handling
        ```python
        try:
            response = requests.get('https://api.github.com/invalid-url')
            response.raise_for_status()  # Raises HTTPError for bad responses
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred: {err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!')
        ```

        ## Timeouts
        ```python
        try:
            response = requests.get('https://api.github.com', timeout=5)
        except requests.exceptions.Timeout:
            print('The request timed out')
        ```

        ## Try It Yourself
        Use the `requests` module in the code editor below to interact with web APIs. Try making GET and POST requests, handling JSON data, and managing errors.
    """)
    display_text(content_text, requests_content)

    # Pre-fill the code editor with sample code
    code_entry.delete('1.0', tk.END)
    sample_code = textwrap.dedent("""
import requests

# Example: Making a GET request
response = requests.get('https://api.github.com')
print(f'Status Code: {response.status_code}')
print(f'Response Body:\\n{response.text[:200]}...')

# Example: Making a POST request
payload = {'key1': 'value1', 'key2': 'value2'}
response = requests.post('https://httpbin.org/post', data=payload)
print(f'POST Response:\\n{response.text[:200]}...')

# Handling JSON data
json_response = requests.get('https://api.github.com')
data = json_response.json()
print(f"Current User URL: {data['current_user_url']}")

# Error handling
try:
    bad_response = requests.get('https://api.github.com/invalid-endpoint')
    bad_response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f'HTTP error occurred: {err}')
except Exception as err:
    print(f'Other error occurred: {err}')
else:
    print('Success!')

# Timeout handling
try:
    slow_response = requests.get('https://httpbin.org/delay/10', timeout=5)
except requests.exceptions.Timeout:
    print('The request timed out')
""")
    code_entry.insert(tk.END, sample_code)

def json_module():
    """Displays the JSON Module content."""
    clear_text(content_text)
    json_content = textwrap.dedent("""
        # JSON Module

        The `json` module in Python provides functions for working with JSON data, allowing you to encode and decode JSON data easily.

        ## Importing JSON
        ```python
        import json
        ```

        ## Parsing JSON
        Convert a JSON string to a Python dictionary.
        ```python
        json_str = '{"name": "Alice", "age": 30, "city": "New York"}'
        data = json.loads(json_str)
        print(data['name'])  # Outputs: Alice
        ```

        ## Serializing JSON
        Convert a Python dictionary to a JSON string.
        ```python
        data = {
            "name": "Bob",
            "age": 25,
            "city": "Los Angeles"
        }
        json_str = json.dumps(data)
        print(json_str)  # Outputs: {"name": "Bob", "age": 25, "city": "Los Angeles"}
        ```

        ## Writing JSON to a File
        ```python
        data = {
            "name": "Charlie",
            "age": 28,
            "city": "Chicago"
        }
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        ```

        ## Reading JSON from a File
        ```python
        with open('data.json', 'r') as f:
            data = json.load(f)
            print(data['city'])  # Outputs: Chicago
        ```

        ## Pretty Printing JSON
        ```python
        data = {
            "name": "Diana",
            "age": 22,
            "city": "Houston",
            "hobbies": ["reading", "gaming", "hiking"]
        }
        pretty_json = json.dumps(data, indent=4)
        print(pretty_json)
        ```

        ## Try It Yourself
        Use the `json` module in the code editor below to parse JSON strings, serialize Python dictionaries, and work with JSON files.
    """)
    display_text(content_text, json_content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
import json

# Parsing JSON string
json_str = '{"title": "Python", "version": 3.9, "features": ["Easy to Learn", "Versatile", "Community Support"]}'
data = json.loads(json_str)
print(f"Title: {data['title']}")
print(f"Version: {data['version']}")
print(f"Features: {', '.join(data['features'])}")

# Serializing Python dictionary to JSON string
python_dict = {
    "name": "Eve",
    "age": 35,
    "languages": ["English", "Spanish", "French"]
}
json_output = json.dumps(python_dict, indent=2)
print(json_output)

# Writing JSON to a file
with open('user_data.json', 'w') as f:
    json.dump(python_dict, f, indent=4)
    print("JSON data written to user_data.json")

# Reading JSON from a file
with open('user_data.json', 'r') as f:
    user_data = json.load(f)
    print(f"User's second language: {user_data['languages'][1]}")

# Pretty printing JSON
pretty_json = json.dumps(user_data, indent=4)
print("Pretty JSON:")
print(pretty_json)
""")

def ctypes_module():
    """Displays the ctypes Module content."""
    clear_text(content_text)
    ctypes_content = textwrap.dedent("""
        # ctypes Module

        The `ctypes` module in Python provides C compatible data types and allows calling functions in DLLs or shared libraries. It can be used to wrap these libraries in pure Python.

        ## Importing ctypes
        ```python
        import ctypes
        ```

        ## Using ctypes to Call C Functions
        Suppose you have a C library `mathlib.so` with a function `int add(int a, int b)`.

        ```c
        // mathlib.c
        int add(int a, int b) {
            return a + b;
        }
        ```

        After compiling the C code into a shared library, you can use ctypes to call it.

        ```python
        import ctypes

        # Load the shared library
        mathlib = ctypes.CDLL('./mathlib.so')

        # Specify argument and return types
        mathlib.add.argtypes = (ctypes.c_int, ctypes.c_int)
        mathlib.add.restype = ctypes.c_int

        # Call the C function
        result = mathlib.add(5, 3)
        print(f'Result of add(5, 3): {result}')  # Outputs: Result of add(5, 3): 8
        ```

        ## Accessing System-Level Functions
        ```python
        import ctypes

        # Get the current process ID
        getpid = ctypes.CDLL(None).getpid
        getpid.restype = ctypes.c_int
        pid = getpid()
        print(f'Current Process ID: {pid}')
        ```

        ## Working with Structures
        ```python
        import ctypes

        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_int),
                        ("y", ctypes.c_int)]

        p = POINT(10, 20)
        print(f'Point coordinates: ({p.x}, {p.y})')
        ```

        ## Try It Yourself
        Use the `ctypes` module in the code editor below to interact with C libraries or system-level functions. **Ensure you have the necessary shared libraries and understand the implications** of calling low-level functions.
    """)
    display_text(content_text, ctypes_content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
import ctypes

# Example: Using ctypes to call the C standard library's printf function
libc = ctypes.CDLL(None)
libc.printf(b"Hello from ctypes!\\n")

# Example: Accessing system-level information
getpid = libc.getpid
getpid.restype = ctypes.c_int
pid = getpid()
print(f'Current Process ID: {pid}')

# Example: Working with structures
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]

p = POINT(100, 200)
print(f'Point coordinates: ({p.x}, {p.y})')
""")

def psutil_module():
    """Displays the psutil Module content."""
    if psutil is None:
        clear_text(content_text)
        psutil_content = textwrap.dedent("""
            # psutil Module

            The `psutil` module in Python provides an interface for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in a portable way.

            ## Installation
            ```bash
            pip install psutil
            ```

            ## Importing psutil
            ```python
            import psutil
            ```

            ## CPU Information
            ```python
            print(f'CPU Count: {psutil.cpu_count(logical=True)}')
            print(f'CPU Usage: {psutil.cpu_percent(interval=1)}%')
            ```

            ## Memory Information
            ```python
            memory = psutil.virtual_memory()
            print(f'Total Memory: {memory.total / (1024 ** 3):.2f} GB')
            print(f'Available Memory: {memory.available / (1024 ** 3):.2f} GB')
            print(f'Used Memory: {memory.used / (1024 ** 3):.2f} GB')
            print(f'Memory Usage: {memory.percent}%')
            ```

            ## Disk Information
            ```python
            disk = psutil.disk_usage('/')
            print(f'Total Disk Space: {disk.total / (1024 ** 3):.2f} GB')
            print(f'Used Disk Space: {disk.used / (1024 ** 3):.2f} GB')
            print(f'Disk Usage: {disk.percent}%')
            ```

            ## Network Information
            ```python
            net_io = psutil.net_io_counters()
            print(f'Bytes Sent: {net_io.bytes_sent}')
            print(f'Bytes Received: {net_io.bytes_recv}')
            ```

            ## Process Information
            ```python
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                print(proc.info)
            ```

            ## Try It Yourself
            Use the `psutil` module in the code editor below to monitor system resources, retrieve process information, and manage system operations.
        """)
        display_text(content_text, psutil_content)
        code_entry.delete('1.0', tk.END)
        code_entry.insert(tk.END, """
import psutil

# CPU Information
cpu_count = psutil.cpu_count(logical=True)
cpu_usage = psutil.cpu_percent(interval=1)
print(f'CPU Count: {cpu_count}')
print(f'CPU Usage: {cpu_usage}%')

# Memory Information
memory = psutil.virtual_memory()
print(f'Total Memory: {memory.total / (1024 ** 3):.2f} GB')
print(f'Available Memory: {memory.available / (1024 ** 3):.2f} GB')
print(f'Used Memory: {memory.used / (1024 ** 3):.2f} GB')
print(f'Memory Usage: {memory.percent}%')

# Disk Information
disk = psutil.disk_usage('/')
print(f'Total Disk Space: {disk.total / (1024 ** 3):.2f} GB')
print(f'Used Disk Space: {disk.used / (1024 ** 3):.2f} GB')
print(f'Disk Usage: {disk.percent}%')

# Network Information
net_io = psutil.net_io_counters()
print(f'Bytes Sent: {net_io.bytes_sent}')
print(f'Bytes Received: {net_io.bytes_recv}')

# Process Information
print("Running Processes:")
for proc in psutil.process_iter(['pid', 'name', 'username']):
    print(proc.info)
""")
    else:
        # If psutil is installed, provide content
        clear_text(content_text)
        psutil_content = textwrap.dedent("""
            # psutil Module

            The `psutil` module in Python provides an interface for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in a portable way.

            ## Importing psutil
            ```python
            import psutil
            ```

            ## CPU Information
            ```python
            print(f'CPU Count: {psutil.cpu_count(logical=True)}')
            print(f'CPU Usage: {psutil.cpu_percent(interval=1)}%')
            ```

            ## Memory Information
            ```python
            memory = psutil.virtual_memory()
            print(f'Total Memory: {memory.total / (1024 ** 3):.2f} GB')
            print(f'Available Memory: {memory.available / (1024 ** 3):.2f} GB')
            print(f'Used Memory: {memory.used / (1024 ** 3):.2f} GB')
            print(f'Memory Usage: {memory.percent}%')
            ```

            ## Disk Information
            ```python
            disk = psutil.disk_usage('/')
            print(f'Total Disk Space: {disk.total / (1024 ** 3):.2f} GB')
            print(f'Used Disk Space: {disk.used / (1024 ** 3):.2f} GB')
            print(f'Disk Usage: {disk.percent}%')
            ```

            ## Network Information
            ```python
            net_io = psutil.net_io_counters()
            print(f'Bytes Sent: {net_io.bytes_sent}')
            print(f'Bytes Received: {net_io.bytes_recv}')
            ```

            ## Process Information
            ```python
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                print(proc.info)
            ```

            ## Try It Yourself
            Use the `psutil` module in the code editor below to monitor system resources, retrieve process information, and manage system operations.
        """)
        display_text(content_text, psutil_content)
        code_entry.delete('1.0', tk.END)
        code_entry.insert(tk.END, """
import psutil

# CPU Information
cpu_count = psutil.cpu_count(logical=True)
cpu_usage = psutil.cpu_percent(interval=1)
print(f'CPU Count: {cpu_count}')
print(f'CPU Usage: {cpu_usage}%')

# Memory Information
memory = psutil.virtual_memory()
print(f'Total Memory: {memory.total / (1024 ** 3):.2f} GB')
print(f'Available Memory: {memory.available / (1024 ** 3):.2f} GB')
print(f'Used Memory: {memory.used / (1024 ** 3):.2f} GB')
print(f'Memory Usage: {memory.percent}%')

# Disk Information
disk = psutil.disk_usage('/')
print(f'Total Disk Space: {disk.total / (1024 ** 3):.2f} GB')
print(f'Used Disk Space: {disk.used / (1024 ** 3):.2f} GB')
print(f'Disk Usage: {disk.percent}%')

# Network Information
net_io = psutil.net_io_counters()
print(f'Bytes Sent: {net_io.bytes_sent}')
print(f'Bytes Received: {net_io.bytes_recv}')

# Process Information
print("Running Processes:")
for proc in psutil.process_iter(['pid', 'name', 'username']):
    print(proc.info)
""")

def subprocess_module():
    """Displays the Subprocess Module content."""
    clear_text(content_text)
    subprocess_content = textwrap.dedent("""
        # Subprocess Module

        The `subprocess` module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. It's a powerful tool for interacting with system commands and external applications.

        ## Importing subprocess
        ```python
        import subprocess
        ```

        ## Running a Simple Command
        ```python
        result = subprocess.run(['echo', 'Hello, Subprocess!'], capture_output=True, text=True)
        print(result.stdout)  # Outputs: Hello, Subprocess!
        ```

        ## Capturing Output
        ```python
        result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
        print(result.stdout)
        ```

        ## Handling Errors
        ```python
        try:
            subprocess.run(['false'], check=True)
        except subprocess.CalledProcessError:
            print('An error occurred while running the command.')
        ```

        ## Piping Commands
        ```python
        ls = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
        grep = subprocess.Popen(['grep', 'py'], stdin=ls.stdout, stdout=subprocess.PIPE, text=True)
        ls.stdout.close()
        output, _ = grep.communicate()
        print(output)
        ```

        ## Running Shell Commands
        **Note:** Be cautious when using `shell=True` as it can pose security risks.
        ```python
        result = subprocess.run('echo Shell Command', shell=True, capture_output=True, text=True)
        print(result.stdout)  # Outputs: Shell Command
        ```

        ## Try It Yourself
        Use the `subprocess` module in the code editor below to execute system commands, capture outputs, handle errors, and interact with external applications.
    """)
    display_text(content_text, subprocess_content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, """
import subprocess

# Running a simple echo command
result = subprocess.run(['echo', 'Hello, Subprocess!'], capture_output=True, text=True)
print(result.stdout)

# Listing directory contents
try:
    result = subprocess.run(['ls', '-l'], capture_output=True, text=True, check=True)
    print(result.stdout)
except subprocess.CalledProcessError:
    print('Failed to list directory contents.')

# Handling errors with a failing command
try:
    subprocess.run(['false'], check=True)
except subprocess.CalledProcessError:
    print('An error occurred while running the command.')

# Piping commands: ls -l | grep py
ls = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
grep = subprocess.Popen(['grep', 'py'], stdin=ls.stdout, stdout=subprocess.PIPE, text=True)
ls.stdout.close()
output, _ = grep.communicate()
print(output)

# Running a shell command
result = subprocess.run('echo Shell Command', shell=True, capture_output=True, text=True)
print(result.stdout)
""")

def show_resources():
    """Displays additional learning resources."""
    clear_text(content_text)
    resources = textwrap.dedent("""
        # Additional Learning Resources

        - [Python Official Documentation](https://docs.python.org/3/)
        - [Real Python Tutorials](https://realpython.com/)
        - [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/)
        - [Python Crash Course by Eric Matthes](https://nostarch.com/pythoncrashcourse2e)
    """)
    display_text(content_text, resources)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, "")

# ---------------- Placeholder Topic Function ----------------

def placeholder_function():
    """Displays a placeholder message for upcoming content."""
    clear_text(content_text)
    placeholder_content = textwrap.dedent("""
        # Coming Soon!

        This section is under development. Stay tuned for more content.
    """)
    display_text(content_text, placeholder_content)
    code_entry.delete('1.0', tk.END)
    code_entry.insert(tk.END, "")

# ---------------- Syntax Highlighting ----------------

import keyword

def syntax_highlight(event=None):
    """Applies basic syntax highlighting to the code editor."""
    code = code_entry.get("1.0", tk.END)
    code_entry.tag_remove("Keyword", "1.0", tk.END)
    code_entry.tag_remove("String", "1.0", tk.END)
    code_entry.tag_remove("Comment", "1.0", tk.END)

    # Highlight keywords
    for kw in keyword.kwlist:
        start = "1.0"
        while True:
            pos = code_entry.search(r'\b' + kw + r'\b', start, stopindex=tk.END, regexp=True)
            if not pos:
                break
            end = f"{pos}+{len(kw)}c"
            code_entry.tag_add("Keyword", pos, end)
            start = end

    # Highlight strings
    start = "1.0"
    while True:
        pos = code_entry.search(r'\".*?\"', start, stopindex=tk.END, regexp=True)
        if not pos:
            break
        end = code_entry.index(f"{pos} + {len(code_entry.get(pos, pos + ' lineend'))}c")
        code_entry.tag_add("String", pos, end)
        start = end

    # Highlight comments
    start = "1.0"
    while True:
        pos = code_entry.search(r'#.*', start, stopindex=tk.END, regexp=True)
        if not pos:
            break
        end = code_entry.index(f"{pos} + {len(code_entry.get(pos, pos + ' lineend'))}c")
        code_entry.tag_add("Comment", pos, end)
        start = end

    # Define tag styles
    code_entry.tag_configure("Keyword", foreground="blue")
    code_entry.tag_configure("String", foreground="green")
    code_entry.tag_configure("Comment", foreground="grey")

# Bind the syntax_highlight function to key release events
code_entry.bind("<KeyRelease>", syntax_highlight)

# ---------------- Initialize User Progress ----------------

def initialize_progress():
    """Initializes user progress by loading existing data."""
    load_progress()
    update_nav_buttons()

# ---------------- Run the Application ----------------

def main():
    """Main function to run the application."""
    initialize_progress()
    root.mainloop()

# ---------------- Entry Point ----------------

if __name__ == "__main__":
    main()
