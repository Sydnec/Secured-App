import socketserver
import datetime

class TCPServer(socketserver.BaseRequestHandler):
    def __init__(self, time_formatter):
        self.time_formatter = time_formatter

    def handle(self):
        self.data = self.request.recv(1024).strip()
        format_string = self.data.decode('utf-8')
        try:
            now = datetime.datetime.now()
            response = self.time_formatter.format_time(now, format_string)
        except Exception as e:
            response = f"Error: {e}"
        self.request.sendall(response.encode('utf-8'))

    @staticmethod
    def start_server(port, time_formatter):
        server = socketserver.TCPServer(("0.0.0.0", port), lambda *args, **kwargs: TCPServer(time_formatter, *args, **kwargs))
        server.serve_forever()
