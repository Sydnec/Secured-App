import socketserver
import datetime

class TCPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.time_formatter = server.time_formatter
        super().__init__(request, client_address, server)

    def handle(self):
        self.data = self.request.recv(30).strip()
        
        # Décodez les données reçues
        format_string = self.data.decode('utf-8')
        
        # Formatez l'heure actuelle
        now = datetime.datetime.now()
        response = self.time_formatter.format_time(now, format_string)
        
        self.request.sendall(response.encode('utf-8'))

class TCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, time_formatter):
        self.time_formatter = time_formatter
        super().__init__(server_address, RequestHandlerClass)

    @staticmethod
    def start_server(port, time_formatter):
        server = TCPServer(("0.0.0.0", port), TCPRequestHandler, time_formatter)
        server.serve_forever()
