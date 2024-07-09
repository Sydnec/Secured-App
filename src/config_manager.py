import configparser
import os

class ConfigManager:
    CONFIG_FILE = os.path.expanduser('./.config/config.ini')

    def __init__(self):
        self.config = configparser.ConfigParser()

    def load_configuration(self):
        if os.path.exists(self.CONFIG_FILE):
            self.config.read(self.CONFIG_FILE)
        else:
            self.config['Network'] = {'Port': 12345}
            self.save_configuration()

    def get_port(self):
        return self.config.getint('Network', 'Port', fallback=12345)

    def save_configuration(self):
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        with open(self.CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)
