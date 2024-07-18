import tkinter as tk
from tkinter import messagebox
import socket
import ssl

class NetworkClockClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Clock Client")
        self.geometry("300x200")

        self.label = tk.Label(self, text="Client", font=("Helvetica", 24))
        self.label.pack(pady=10)

        self.format_string = tk.StringVar(value="%a %d %b %Y - %H:%M:%S")

        self.time_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.time_label.pack(pady=10)
        
        self.entry = tk.Entry(self, textvariable=self.format_string, width=30, justify="center")
        self.entry.pack(pady=5)
        
        self.update_button = tk.Button(self, text="Update Display", command=self.send_request)
        self.update_button.pack(pady=5)

    def send_request(self):
        server_address = ('localhost', 12345)  # Adresse et port du serveur Network Clock

        try:
            # Création du socket et sécurisation avec SSL
            sock = socket.create_connection(server_address)
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False  # Désactiver la vérification de l'hôte pour localhost
            context.load_verify_locations('../certs/server.crt')
            secure_sock = context.wrap_socket(sock, server_hostname='localhost')

            # Envoi de la requête GET_TIME avec le format spécifié
            request = f"GET_TIME {self.format_string.get()}"
            secure_sock.sendall(request.encode('utf-8'))

            # Réception de la réponse
            response = secure_sock.recv(1024).decode('utf-8')
            self.time_label.config(text=response)

            secure_sock.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

if __name__ == "__main__":
    app = NetworkClockClient()
    app.mainloop()