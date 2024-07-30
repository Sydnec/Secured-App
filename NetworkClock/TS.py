import sys
import ctypes
from datetime import datetime

def validate_datetime_string(datetime_string):
    try:
        datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def set_system_time(new_time_str):
    try:
        new_time = datetime.strptime(new_time_str, "%Y-%m-%d %H:%M:%S")

        class SYSTEMTIME(ctypes.Structure):
            _fields_ = [("wYear", ctypes.c_uint16),
                        ("wMonth", ctypes.c_uint16),
                        ("wDayOfWeek", ctypes.c_uint16),
                        ("wDay", ctypes.c_uint16),
                        ("wHour", ctypes.c_uint16),
                        ("wMinute", ctypes.c_uint16),
                        ("wSecond", ctypes.c_uint16),
                        ("wMilliseconds", ctypes.c_uint16)]

        # Calculate the day of the week for SYSTEMTIME
        wDayOfWeek = (new_time.weekday() + 1) % 7

        system_time = SYSTEMTIME(new_time.year, new_time.month, new_time.day, wDayOfWeek, new_time.hour, new_time.minute, new_time.second, 0)
        # Call Windows API to set system time
        result = ctypes.windll.kernel32.SetSystemTime(ctypes.byref(system_time))
        if result == 0:
            raise ctypes.WinError()
        print("System time set successfully.")
    except ValueError:
        print("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")
    except Exception:
        print("Failed to set system time due to an unexpected error.")

def enable_DEP():
    try:
        # Enable DEP using SetProcessDEPPolicy
        ctypes.windll.kernel32.SetProcessDEPPolicy(1)
    except Exception as e:
        print(f"Failed to enable DEP: {e}")

if __name__ == "__main__":
    # Enable DEP
    enable_DEP()

    if len(sys.argv) != 2:
        print("Usage: python TS.py 'YYYY-MM-DD HH:MM:SS'")
        sys.exit(1)

    new_time_str = sys.argv[1]
    if validate_datetime_string(new_time_str):
        set_system_time(new_time_str)
    else:
        print("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'")