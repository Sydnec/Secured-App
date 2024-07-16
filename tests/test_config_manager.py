import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import configparser
from src.config_manager import ConfigManager  # Assurez-vous que le nom du module est correct

class TestConfigManager(unittest.TestCase):

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_load_configuration_file_exists(self, mock_makedirs, mock_open, mock_exists):
        mock_exists.return_value = True

        config_manager = ConfigManager()
        config_manager.load_configuration()

        mock_open.assert_called_once_with(config_manager.CONFIG_FILE, encoding='locale')
        mock_makedirs.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_load_configuration_file_not_exists(self, mock_makedirs, mock_open, mock_exists):
        mock_exists.return_value = False

        config_manager = ConfigManager()
        config_manager.load_configuration()

        mock_makedirs.assert_called_once_with(os.path.dirname(config_manager.CONFIG_FILE), exist_ok=True)
        mock_open.assert_called_once_with(config_manager.CONFIG_FILE, 'w')
        self.assertEqual(config_manager.get_port(), 12345)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_get_port(self, mock_makedirs, mock_open, mock_exists):
        mock_exists.return_value = True

        config_manager = ConfigManager()
        config_manager.config.read_dict({'Network': {'Port': '54321'}})
        
        port = config_manager.get_port()
        self.assertEqual(port, 54321)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_save_configuration(self, mock_makedirs, mock_open):
        config_manager = ConfigManager()
        config_manager.save_configuration()

        mock_makedirs.assert_called_once_with(os.path.dirname(config_manager.CONFIG_FILE), exist_ok=True)
        mock_open.assert_called_once_with(config_manager.CONFIG_FILE, 'w')

if __name__ == '__main__':
    unittest.main()
