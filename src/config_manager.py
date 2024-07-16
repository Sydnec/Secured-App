import os
import configparser 

class ConfigManager:
    CONFIG_FILE = os.path.expanduser('./.config/config.ini')

    def __init__(self):
        self.config = configparser.ConfigParser()

    def load_configuration(self):
        if os.path.exists(self.CONFIG_FILE):
            self._check_permissions()
            self.config.read(self.CONFIG_FILE)
        else:
            self.config['Network'] = {'Port': 12345}
            self.save_configuration()
        self.validate_configuration()

    def get_port(self):
        return self.config.getint('Network', 'Port', fallback=12345)

    def save_configuration(self):
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        with open(self.CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def validate_configuration(self):
        port = self.config.getint('Network', 'Port', fallback=None)
        if port is None or not (1 <= port <= 65535):
            raise ValueError("Invalid port number in configuration file")

    def _check_permissions(self):
        if not os.access(self.CONFIG_FILE, os.R_OK):
            raise PermissionError(f"No read permission for {self.CONFIG_FILE}")
        if not os.access(self.CONFIG_FILE, os.W_OK):
            raise PermissionError(f"No write permission for {self.CONFIG_FILE}")