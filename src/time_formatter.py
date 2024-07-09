import datetime

class TimeFormatter:
    def __init__(self):
        pass
    
    def format_time(self, dt, format_string):
        format_string = self._convert_custom_format(format_string)
        return dt.strftime(format_string)
    
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
