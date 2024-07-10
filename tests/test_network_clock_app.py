import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import simpledialog, messagebox
import datetime
from src.network_clock_app import NetworkClockApp
from src.time_formatter import TimeFormatter
from src.time_setter import TimeSetter

class TestNetworkClockApp(unittest.TestCase):
    def setUp(self):
        self.app = NetworkClockApp(TimeFormatter())

    def test_update_display_valid_format(self):
        self.app.format_string.set("WWW DD MMM YYYY - HH:mm:SS")
        self.app.time_formatter.format_time = MagicMock(return_value="Mocked Time")
        self.app.update_display()
        self.assertEqual(self.app.label.cget('text'), "Mocked Time")

    @patch('tkinter.simpledialog.askstring', return_value="2023 07 10 12 30 00")
    @patch('tkinter.messagebox.showinfo')
    def test_set_datetime_success(self, mock_showinfo, mock_askstring):
        TimeSetter.set_system_time = MagicMock()
        self.app.set_datetime()
        TimeSetter.set_system_time.assert_called_once_with("2023 07 10 12 30 00")
        mock_showinfo.assert_called_once_with("Success", "System time updated successfully.")

    @patch('tkinter.simpledialog.askstring', side_effect=Exception("Mocked Exception"))
    @patch('tkinter.messagebox.showerror')
    def test_set_datetime_failure(self, mock_showerror, mock_askstring):
        TimeSetter.set_system_time = MagicMock()
        self.app.set_datetime()
        mock_showerror.assert_called_once_with("Error", "Failed to set system time: Mocked Exception")

if __name__ == '__main__':
    unittest.main()

