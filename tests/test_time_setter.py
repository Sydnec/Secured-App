import unittest
from unittest.mock import patch, MagicMock
import sys
import datetime

# Ajoutez le chemin du répertoire src au PYTHONPATH pour que les importations fonctionnent correctement
sys.path.append("src")

# Importez la classe TimeSetter à partir du module approprié
from time_setter import TimeSetter

class TestTimeSetter(unittest.TestCase):

    @patch('time_setter.messagebox.showerror')
    def test_invalid_time_format(self, mock_showerror):
        TimeSetter.set_system_time("invalid time")
        mock_showerror.assert_called_once_with("Error", "Invalid date/time format. Please use YYYY MM DD HH mm SS.")

    @patch('sys.platform', 'win32')
    @patch('time_setter.TimeSetter.set_system_time_win')
    def test_set_time_windows(self, mock_set_time_win):
        TimeSetter.set_system_time("2023 07 10 12 00 00")
        mock_set_time_win.assert_called_once()

    @patch('sys.platform', 'linux')
    @patch('time_setter.TimeSetter.set_system_time_unix')
    def test_set_time_linux(self, mock_set_time_unix):
        TimeSetter.set_system_time("2023 07 10 12 00 00")
        mock_set_time_unix.assert_called_once_with("2023-07-10 12:00:00")

    @patch('sys.platform', 'darwin')
    @patch('time_setter.TimeSetter.set_system_time_macos')
    def test_set_time_macos(self, mock_set_time_macos):
        TimeSetter.set_system_time("2023 07 10 12 00 00")
        mock_set_time_macos.assert_called_once_with("071012002023.00")

    @patch('sys.platform', 'unsupported_platform')
    @patch('time_setter.messagebox.showerror')
    def test_unsupported_platform(self, mock_showerror):
        with self.assertRaises(NotImplementedError):
            TimeSetter.set_system_time("2023 07 10 12 00 00")
        mock_showerror.assert_called_once_with("Platform 'unsupported_platform' not supported for setting system time.")

    @patch('subprocess.run')
    @patch('sys.platform', 'linux')
    def test_set_system_time_unix(self, mock_run):
        TimeSetter.set_system_time_unix("2023-07-10 12:00:00")
        mock_run.assert_called_once_with(["sudo", "date", "--set", "2023-07-10 12:00:00"], check=True)

    @patch('subprocess.run')
    @patch('sys.platform', 'darwin')
    def test_set_system_time_macos(self, mock_run):
        TimeSetter.set_system_time_macos("071012002023.00")
        mock_run.assert_called_once_with(['sudo', 'date', '071012002023.00'], check=True)

if __name__ == '__main__':
    unittest.main()
