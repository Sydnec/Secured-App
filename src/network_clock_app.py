import subprocess
import datetime
import re
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from time_formatter import TimeFormatter

class NetworkClockApp(tk.Tk):
    def __init__(self, time_formatter):
        super().__init__()
        self.title("Network Clock")
        self.geometry("300x250")
        self.time_formatter = time_formatter

        self.label = tk.Label(self, text="Server", font=("Helvetica", 24))
        self.label.pack(pady=10)

        self.format_string = tk.StringVar(value="WWW DD MMM YYYY - HH:mm:SS")
        
        self.label = tk.Label(self, text="", font=("Helvetica", 16))
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(self, textvariable=self.format_string, width=30, justify="center")
        self.entry.pack(pady=5)
        
        self.update_button = tk.Button(self, text="Update Display", command=self.update_display)
        self.update_button.pack(pady=5)
        
        self.set_button = tk.Button(self, text="Set Date/Time", command=self.set_datetime)
        self.set_button.pack(pady=5)
    
    def update_display(self):
        now = datetime.datetime.now()
        formatted_time = self.time_formatter.format_time(now, self.format_string.get())
        self.label.config(text=formatted_time)

    def set_datetime(self):
        user_input = simpledialog.askstring("Set Date/Time", "Enter new date and time (YYYY MM DD HH mm SS):")
        
        if not re.match(r"^\d{4} \d{2} \d{2} \d{2} \d{2} \d{2}$", user_input):
            messagebox.showerror("Error", "Invalid date/time format. Please use YYYY MM DD HH mm SS.")
            return
        
        try:
            new_time = datetime.datetime.strptime(user_input, "%Y %m %d %H %M %S")
            new_time_str = new_time.strftime("%Y-%m-%d %H:%M:%S")
            script_file = 'src/time_setter.py'
            
            if sys.platform == 'win32':
                subprocess.run(['runas', '/user:Administrator', 'python', script_file, new_time_str], check=True)
            elif sys.platform.startswith('linux') or sys.platform == 'darwin':
                subprocess.run(['sudo', 'python3', script_file, new_time_str], check=True)
            else:
                raise NotImplementedError(f"Unsupported platform: {sys.platform}")
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format. Please use YYYY MM DD HH mm SS.")
