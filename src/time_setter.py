import sys
import subprocess
import datetime

class TimeSetter:
    @staticmethod
    def set_system_time(new_time_str):
        try:
            new_time = datetime.datetime.strptime(new_time_str, "%Y %m %d %H %M %S")
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format. Please use YYYY MM DD HH mm SS.")

        if sys.platform == "win32":
            new_system_time = (new_time.year, new_time.month, new_time.day, 
                new_time.hour, new_time.minute, new_time.second, 
                new_time.microsecond // 1000, -1)
            TimeSetter.set_system_time_win(new_system_time)
        elif sys.platform.startswith("linux"):
            TimeSetter.set_system_time_unix(new_time.strftime("%Y-%m-%d %H:%M:%S"))
        elif sys.platform == "darwin":
            TimeSetter.set_system_time_macos(new_time.strftime("%m%d%H%M%Y.%S"))
        else:
            raise NotImplementedError(f"Platform '{sys.platform}' not supported for setting system time.")

    @staticmethod
    def set_system_time_win(new_system_time):
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
            wYear=new_system_time[0],
            wMonth=new_system_time[1],
            wDay=new_system_time[2],
            wHour=new_system_time[3],
            wMinute=new_system_time[4],
            wSecond=new_system_time[5],
            wMilliseconds=new_system_time[6],
        )

        # Use the appropriate Windows API to set the system time
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
