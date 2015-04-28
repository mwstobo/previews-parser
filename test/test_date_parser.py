import unittest
import previews_parser
import datetime

class DateParserTest(unittest.TestCase):
    def test_simple_parsing(self):
        string = 'New Releases for 4/25/2015'
        output = previews_parser.parse_date(string)
        expected = datetime.date(2015, 4, 25)
        self.assertEquals(output, expected)

    def test_simple_parsing_again(self):
        string = 'New Releases for 1/1/2015'
        output = previews_parser.parse_date(string)
        expected = datetime.date(2015, 1, 1)
        self.assertEquals(output, expected)

    def test_two_dates(self):
        string = 'New Releases for 1/1/2015\n5/4/2014'
        output = previews_parser.parse_date(string)
        expected = datetime.date(2015, 1, 1)
        self.assertEquals(output, expected)

    def test_no_match(self):
        string = 'New Releases for 1/1'
        output = previews_parser.parse_date(string)
        expected = None
        self.assertEquals(output, expected)
