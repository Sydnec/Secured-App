import tkinter as tk
from tkinter import messagebox
import socket
import threading
import datetime
import subprocess
import platform
import ssl
import re
import configparser
import sys
import os
import ctypes

class NetworkClock(tk.Tk):
    def __init__(self):
        super().__init__()

        # Verify Windows OS
        if platform.system() != 'Windows':
            messagebox.showerror("Error", "This application only supports Windows.")
            sys.exit(1)

        # Enable DEP
        self.enable_DEP()

        # Secure configuration file and TS.py path
        appdata_path = os.path.join(os.getenv('APPDATA'), 'NetworkClock')
        config_path = os.path.join(appdata_path, 'config.ini')
        self.ts_script_path = os.path.join(appdata_path, 'TS.py')

        if not os.path.exists(config_path):
            messagebox.showerror("Error", f"The required file {config_path} does not exist.")
            sys.exit(1)

        # Check if TS.py exists
        if not os.path.exists(self.ts_script_path):
            messagebox.showerror("Error", f"The required script {self.ts_script_path} does not exist.")
            sys.exit(1)

        # Initialize the ConfigParser
        config = configparser.ConfigParser()

        # Read the config.ini file
        config.read(config_path)

        # Validate the port from the config file
        port = config.get('server', 'port')
        if not self.validate_port(port):
            messagebox.showerror("Error", "Invalid port number in config file.")
            sys.exit(1)

        # Get the port as an integer
        self.port = int(port)

        self.create_GUI()
        self.update_display()
        self.start_server()

    def create_GUI(self):
        self.title("Network Clock")
        self.geometry("300x250")
        self.format_string = tk.StringVar(value="%a %d %b %Y - %H:%M:%S")

        self.label = tk.Label(self, text="Server", font=("Helvetica", 24))
        self.label.pack(pady=10)

        self.time_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.time_label.pack(pady=10)

        self.entry = tk.Entry(self, textvariable=self.format_string, width=30, justify="center")
        self.entry.pack(pady=5)

        self.update_button = tk.Button(self, text="Update Display", command=self.update_display)
        self.update_button.pack(pady=5)

        self.set_button = tk.Button(self, text="Set Date/Time", command=self.set_datetime)
        self.set_button.pack(pady=5)

    def validate_port(self, port):
        try:
            port = int(port)
            return 1 <= port <= 65535
        except ValueError:
            return False

    def validate_format_string(self, format_string):
        # Allow only valid date/time format characters
        allowed_chars = re.compile(r'^[%a-zA-Z0-9\s\-\:\./]+$')
        return bool(allowed_chars.match(format_string))

    def validate_datetime_string(self, datetime_string):
        try:
            # Check if the datetime string matches the format 'YYYY-MM-DD HH:MM:SS'
            dt = datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
            # Additional validation to ensure it's a valid datetime
            if datetime_string != dt.strftime("%Y-%m-%d %H:%M:%S"):
                raise ValueError
            return True
        except ValueError:
            return False

    def update_display(self):
        if self.validate_format_string(self.format_string.get()):
            current_time = datetime.datetime.now().strftime(self.format_string.get())
            self.time_label.config(text=current_time)
        else:
            messagebox.showerror("Error", "Invalid format string.")

    def set_datetime(self):
        new_time = self.format_string.get()
        if self.validate_datetime_string(new_time):
            try:
                if platform.system() == 'Windows':
                    # Use TS.py script to set system time on Windows
                    new_time_obj = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
                    subprocess.run([sys.executable, self.ts_script_path, new_time_obj.strftime("%Y-%m-%d %H:%M:%S")], check=True)
                    messagebox.showinfo("Success", "Time set successfully.")
                else:
                    messagebox.showerror("Error", "This operation is only supported on Windows.")
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to set time.")
        else:
            messagebox.showerror("Error", "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', self.port))
        self.server.listen(5)

        # SSL Configuration
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="./certs/server.crt", keyfile="./certs/server.key")

        self.server_thread = threading.Thread(target=self.run_server, args=(context,))
        self.server_thread.daemon = True
        self.server_thread.start()

    def run_server(self, context):
        while True:
            client_socket, addr = self.server.accept()
            secure_socket = context.wrap_socket(client_socket, server_side=True)
            client_handler = threading.Thread(target=self.handle_client, args=(secure_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        buffer = ""
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    self.process_message(client_socket, message.strip())
            except Exception:
                client_socket.send(b"An error occurred.")
                break
        client_socket.close()

    def process_message(self, client_socket, message):
        try:
            if message.startswith("GET_TIME"):
                _, format_string = message.split(' ', 1)
                if self.validate_format_string(format_string):
                    current_time = datetime.datetime.now().strftime(format_string)
                    client_socket.send((current_time + '\n').encode('utf-8'))
                else:
                    client_socket.send(b"Invalid format string.\n")
            else:
                client_socket.send(b"Invalid command.\n")
        except Exception:
            client_socket.send(b"An error occurred.\n")

    def enable_DEP(self):
        try:
            # Enable DEP using SetProcessDEPPolicy
            ctypes.windll.kernel32.SetProcessDEPPolicy(1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enable DEP: {e}")

if __name__ == "__main__":
    app = NetworkClock()
    app.mainloop()
