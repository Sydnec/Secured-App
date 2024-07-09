import threading
from config_manager import ConfigManager
from network_clock_app import NetworkClockApp
from tcp_server import TCPServer
from time_formatter import TimeFormatter

def main():
    # Load configuration
    config_manager = ConfigManager()
    config_manager.load_configuration()
    port = config_manager.get_port()

    # Initialize TimeFormatter
    time_formatter = TimeFormatter()

    # Start TCP Server in a separate thread
    server_thread = threading.Thread(target=TCPServer.start_server, args=(port, time_formatter), daemon=True)
    server_thread.start()

    # Start the GUI application
    app = NetworkClockApp(time_formatter)
    app.mainloop()

if __name__ == "__main__":
    main()
