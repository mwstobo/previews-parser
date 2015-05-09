import unittest
import previews_parser
import urllib.request
import urllib.error
from unittest.mock import MagicMock

class ImageFinderTest(unittest.TestCase):
    def setUp(self):
        self.file_mock = MagicMock()
        urllib.request.urlopen = MagicMock(return_value=self.file_mock)
        self.BASE_URL = 'http://www.previewsworld.com/'

    def test_parses_for_correct_image(self):
        publisher = 'DC Comics'
        code = 'abc123456'
        f_string = "<div class='StockCodeImage'><img src='test'></img></div>"
        self.file_mock.read.return_value = f_string
        output = previews_parser.get_image_location(publisher, code)
        expected = self.BASE_URL + 'test'
        self.assertEquals(output, expected)

    def test_no_image_src(self):
        publisher = 'DC Comics'
        code = 'abc123456'
        f_string = "<div class='StockCodeImage'><img src></img></div>"
        self.file_mock.read.return_value = f_string
        with self.assertRaisesRegex(previews_parser.ImageFinderError, 'image src is empty'):
            previews_parser.get_image_location(publisher, code)

    def test_no_cover(self):
        publisher = 'DC Comics'
        code = 'abc123456'
        f_string = "<div class='StockCodeImage'></div>"
        self.file_mock.read.return_value = f_string
        with self.assertRaisesRegex(previews_parser.ImageFinderError, 'no image found'):
            previews_parser.get_image_location(publisher, code)

    def test_no_cover_div(self):
        publisher = 'DC Comics'
        code = 'abc123456'
        f_string = "<div></div>"
        self.file_mock.read.return_value = f_string
        with self.assertRaisesRegex(previews_parser.ImageFinderError, 'no image container found'):
            previews_parser.get_image_location(publisher, code)

    def test_bad_publisher(self):
        publisher = 'bad pub'
        code = 'abc123456'
        with self.assertRaisesRegex(ValueError, 'invalid publisher'):
            previews_parser.get_image_location(publisher, code)

    def test_no_connection(self):
        urllib.request.urlopen = MagicMock(side_effect=urllib.error.URLError(''))
        publisher = 'DC Comics'
        code = 'abc123456'
        with self.assertRaisesRegex(previews_parser.ConnectionError, 'cannot connect to PreviewsWorld'):
            previews_parser.get_image_location(publisher, code)
