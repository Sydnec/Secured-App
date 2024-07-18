import sys
import ctypes
from datetime import datetime
import re

def validate_datetime_string(datetime_string):
    try:
        datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def set_system_time(new_time_str):
    try:
        # Convertir la chaîne de temps en objet datetime
        new_time = datetime.strptime(new_time_str, "%Y-%m-%d %H:%M:%S")

        # Créer une structure SYSTEMTIME
        system_time = ctypes.windll.kernel32.SYSTEMTIME()
        system_time.wYear = new_time.year
        system_time.wMonth = new_time.month
        system_time.wDay = new_time.day
        system_time.wHour = new_time.hour
        system_time.wMinute = new_time.minute
        system_time.wSecond = new_time.second
        system_time.wMilliseconds = 0

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
