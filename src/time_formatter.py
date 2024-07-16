import datetime
import re

class TimeFormatter:
    def __init__(self):
        pass
    
    def format_time(self, dt, format_string):
        format_string = self._convert_custom_format(format_string)
        # Validez le format de la chaîne
        try:
            if not self.is_valid_format_string(format_string):
                raise ValueError("Invalid format string")
            return dt.strftime(format_string)
        except Exception as e:
            return f"Error: {e}"
    
    def is_valid_format_string(self, format_string):
        # Exemples de validation : vérifier la longueur et le contenu de la chaîne
        if len(format_string) > 30:
            return False
        # Vérifiez que la chaîne ne contient que des caractères alphanumériques et certains caractères spéciaux
        if not re.match(r'^[\w\s%:-]*$', format_string):
            return False
        return True

    def _convert_custom_format(self, format_string):
        format_string = format_string.replace("YYYY", "%Y")
        format_string = format_string.replace("YY", "%y")
        format_string = format_string.replace("WWW", "%a")
        format_string = format_string.replace("DD", "%d")
        format_string = format_string.replace("Day", "%A")
        format_string = format_string.replace("MMM", "%b")
        format_string = format_string.replace("MM", "%m")
        format_string = format_string.replace("Month", "%B")
        format_string = format_string.replace("HH", "%H")
        format_string = format_string.replace("mm", "%M")
        format_string = format_string.replace("SS", "%S")
        return format_string
