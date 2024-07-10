import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
from time_formatter import TimeFormatter
from time_setter import TimeSetter

class NetworkClockApp(tk.Tk):
    def __init__(self, time_formatter):
        super().__init__()
        self.title("Network Clock")
        self.geometry("300x200")
        self.time_formatter = time_formatter

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
        try:
            new_time = simpledialog.askstring("Set Date/Time", "Enter new date/time (YYYY MM DD HH mm SS):")
            if new_time:
                new_time = new_time.strip()
                TimeSetter.set_system_time(new_time)
                messagebox.showinfo("Success", "System time updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set system time: {e}")
