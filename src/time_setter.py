import timesetter
from datetime import datetime
import sys

def set_system_time(target_time):
    timesetter.set(target_time)

if __name__ == "__main__":
    try:
        datetime_str = sys.argv[1]
        target_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        set_system_time(target_time)
        print(f"L'heure du système a été définie sur {datetime_str}.")
    except IndexError:
        print("Veuillez fournir une date et une heure au format 'YYYY-MM-DD HH:MM:SS' en argument.")
    except ValueError:
        print("Format de date/heure invalide. Utilisez le format 'YYYY-MM-DD HH:MM:SS'.")
