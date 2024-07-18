import tkinter as tk
from tkinter import messagebox
import socket
import threading
import datetime
import os
import subprocess
import platform
import ssl
import re

class NetworkClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Clock")
        self.geometry("300x250")
        self.format_string = tk.StringVar(value="%a %d %b %Y - %H:%M:%S")
        
        self.create_widgets()
        self.start_server()

    def create_widgets(self):
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

    def validate_format_string(self, format_string):
        # Autoriser uniquement les caractères de format de date/heure valides
        allowed_chars = re.compile(r'^[%a-zA-Z0-9\s\-\:\./]+$')
        if allowed_chars.match(format_string):
            return True
        return False

    def validate_datetime_string(self, datetime_string):
        try:
            datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
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
                    # Exécute le script TS.py pour définir l'heure système sur Windows
                    subprocess.run(['python', 'TS.py', new_time], check=True)
                else:
                    # Utilise la commande 'date' pour définir l'heure sur Unix-like (Linux, macOS)
                    formatted_time = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
                    subprocess.run(['sudo', 'date', formatted_time.strftime('%m%d%H%M%Y.%S')], check=True)
                messagebox.showinfo("Success", "Time set successfully.")
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to set time.")
        else:
            messagebox.showerror("Error", "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")

    def start_server(self):
        user_dir = os.path.expanduser('~')
        config_file_path = os.path.join(user_dir, 'AppData', 'Local', 'Clock', 'port.txt')
        
        # Assurez-vous que le chemin existe ou utilisez un chemin différent si nécessaire
        if not os.path.exists(config_file_path):
            os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
            with open(config_file_path, 'w') as file:
                file.write('12345')  # Utiliser un port par défaut, par exemple 12345
        
        with open(config_file_path, 'r') as file:
            self.port = int(file.read().strip())
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', self.port))
        self.server.listen(5)

        # Configuration SSL
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="../certs/server.crt", keyfile="../certs/server.key")

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
        while True:
            try:
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    break
                if request.startswith("GET_TIME"):
                    _, format_string = request.split(' ', 1)
                    if self.validate_format_string(format_string):
                        current_time = datetime.datetime.now().strftime(format_string)
                        client_socket.send(current_time.encode('utf-8'))
                    else:
                        client_socket.send(b"Invalid format string.")
                elif request.startswith("SET_TIME"):
                    if client_socket.getpeername()[0] == '127.0.0.1':
                        _, new_time = request.split(' ', 1)
                        if self.validate_datetime_string(new_time):
                            if platform.system() == 'Windows':
                                subprocess.run(['python', 'TS.py', new_time])
                            else:
                                formatted_time = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
                                subprocess.run(['sudo', 'date', formatted_time.strftime('%m%d%H%M%Y.%S')])
                            client_socket.send(b"Time set successfully.")
                        else:
                            client_socket.send(b"Invalid date format.")
                    else:
                        client_socket.send(b"Permission denied.")
                else:
                    client_socket.send(b"Invalid command.")
            except Exception as e:
                client_socket.send(f"Error: {e}".encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    app = NetworkClock()
    app.mainloop()
