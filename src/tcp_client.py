import socket
import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

class TCPClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Clock Client")
        self.geometry("300x200")

        self.label = tk.Label(self, text="Client", font=("Helvetica", 24))
        self.label.pack(pady=10)

        self.format_string = tk.StringVar(value="WWW DD MMM YYYY - HH:mm:SS")

        self.label = tk.Label(self, text="", font=("Helvetica", 16))
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(self, textvariable=self.format_string, width=30, justify="center")
        self.entry.pack(pady=5)
        
        self.update_button = tk.Button(self, text="Update Display", command=self.send_request)
        self.update_button.pack(pady=5)        
    
    def send_request(self):
        host = "localhost"
        port = 12345
        format_string = self.format_string.get()
        try:
            response = self.client(host, port, format_string)
            self.label.config(text=response)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def client(self, host, port, format_string):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(format_string.encode('utf-8'))
            response = sock.recv(50)
            sock.close()
            return response.decode('utf-8')

if __name__ == '__main__':
    app = TCPClient()
    app.mainloop()
