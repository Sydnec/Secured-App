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

        system_time = SYSTEMTIME(new_time.year, new_time.month, new_time.day, new_time.weekday(),
                                 new_time.day, new_time.hour, new_time.minute, new_time.second, 0)
        # Appeler l'API Windows pour définir l'heure système
        result = ctypes.windll.kernel32.SetSystemTime(ctypes.byref(system_time))
        if result == 0:
            raise ctypes.WinError()
        print("System time set successfully.")
    except ValueError:
        print("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")
    except Exception as e:
        print(f"Failed to set system time: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python TS.py 'YYYY-MM-DD HH:MM:SS'")
        sys.exit(1)

    new_time_str = sys.argv[1]
    if validate_datetime_string(new_time_str):
        set_system_time(new_time_str)
    else:
        print("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'")
