import unittest
from datetime import datetime
from src.time_formatter import TimeFormatter 

class TestTimeFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = TimeFormatter()
        self.test_datetime = datetime(2024, 7, 10, 12, 34, 56)

    def test_format_time_with_year(self):
        result = self.formatter.format_time(self.test_datetime, "YYYY")
        self.assertEqual(result, "2024")

    def test_format_time_with_short_year(self):
        result = self.formatter.format_time(self.test_datetime, "YY")
        self.assertEqual(result, "24")

    def test_format_time_with_weekday_abbreviation(self):
        result = self.formatter.format_time(self.test_datetime, "WWW")
        self.assertEqual(result, "Wed")

    def test_format_time_with_day(self):
        result = self.formatter.format_time(self.test_datetime, "DD")
        self.assertEqual(result, "10")

    def test_format_time_with_full_weekday_name(self):
        result = self.formatter.format_time(self.test_datetime, "Day")
        self.assertEqual(result, "Wednesday")

    def test_format_time_with_month_abbreviation(self):
        result = self.formatter.format_time(self.test_datetime, "MMM")
        self.assertEqual(result, "Jul")

    def test_format_time_with_month_number(self):
        result = self.formatter.format_time(self.test_datetime, "MM")
        self.assertEqual(result, "07")

    def test_format_time_with_full_month_name(self):
        result = self.formatter.format_time(self.test_datetime, "Month")
        self.assertEqual(result, "July")

    def test_format_time_with_hour(self):
        result = self.formatter.format_time(self.test_datetime, "HH")
        self.assertEqual(result, "12")

    def test_format_time_with_minute(self):
        result = self.formatter.format_time(self.test_datetime, "mm")
        self.assertEqual(result, "34")

    def test_format_time_with_second(self):
        result = self.formatter.format_time(self.test_datetime, "SS")
        self.assertEqual(result, "56")

    def test_format_time_with_combined_format(self):
        format_string = "YYYY-MM-DD HH:mm:SS"
        expected_result = "2024-07-10 12:34:56"
        result = self.formatter.format_time(self.test_datetime, format_string)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
