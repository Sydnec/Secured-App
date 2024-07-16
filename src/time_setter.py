import platform
import subprocess
import datetime
import sys
from tkinter import messagebox

class TimeSetter:
    @staticmethod
    def set_system_time(new_time):
        try:
            if platform.system() == "Windows":
                TimeSetter.set_system_time_win(new_time)
            elif platform.system() == "Linux":
                TimeSetter.set_system_time_unix(new_time.strftime("%Y-%m-%d %H:%M:%S"))
            elif platform.system() == "Darwin":
                TimeSetter.set_system_time_macos(new_time.strftime("%m%d%H%M%Y.%S"))
            else:
                messagebox.showerror(f"Platform '{sys.platform}' not supported for setting system time.")
                raise NotImplementedError(f"Platform '{sys.platform}' not supported for setting system time.")
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format. Please use YYYY MM DD HH mm SS.")

    @staticmethod
    def set_system_time_win(new_time):
        import ctypes
        
        class SYSTEMTIME(ctypes.Structure):
            _fields_ = [
                ("wYear", ctypes.c_ushort),
                ("wMonth", ctypes.c_ushort),
                ("wDayOfWeek", ctypes.c_ushort),
                ("wDay", ctypes.c_ushort),
                ("wHour", ctypes.c_ushort),
                ("wMinute", ctypes.c_ushort),
                ("wSecond", ctypes.c_ushort),
                ("wMilliseconds", ctypes.c_ushort),
            ]

        system_time = SYSTEMTIME(
            wYear=new_time.year,
            wMonth=new_time.month,
            wDay=new_time.day,
            wHour=new_time.hour,
            wMinute=new_time.minute,
            wSecond=new_time.second,
            wMilliseconds=0,
        )

        result = ctypes.windll.kernel32.SetSystemTime(ctypes.byref(system_time))
        if not result:
            raise OSError("Failed to set system time")

    @staticmethod
    def set_system_time_unix(new_time_str):
        try:
            subprocess.run(["sudo", "date", "--set", new_time_str], check=True)
        except subprocess.CalledProcessError as e:
            raise OSError(f"Failed to set system time: {e}")

    @staticmethod
    def set_system_time_macos(new_time_str):
        try:
            subprocess.run(['sudo', 'date', new_time_str], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to set system time on macOS: {e}")
