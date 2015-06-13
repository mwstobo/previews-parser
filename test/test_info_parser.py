import unittest
import previews_parser

class ReleaseInfoParserTest(unittest.TestCase):
    def test_simple_parsing(self):
        string = 'AQUAMAN AND THE OTHERS #11'
        output = previews_parser.parse_release_info(string)
        expected = {
            'series': 'Aquaman And The Others',
            'issue': 11,
        }
        self.assertEquals(output, expected)

    def test_mature_parsing(self):
        string = 'NAMELESS #2 (MR)'
        output = previews_parser.parse_release_info(string)
        expected = {
            'series': 'Nameless',
            'issue': 2,
            'mature': True
        }
        self.assertEquals(output, expected)

    def test_printint(self):
        string = 'NAMELESS #1 2ND PRINTING (MR)'
        output = previews_parser.parse_release_info(string)
        expected = {
            'series': 'Nameless',
            'issue': 1,
            'mature': True,
            'printing': 2
        }
        self.assertEquals(output, expected)

    def test_bad_input(self):
        string = 'DEAD BOY DETECTIVES TP VOL 02 GHOST SNOW'
        output = previews_parser.parse_release_info(string)
        expected = {}
        self.assertEquals(output, expected)

    def test_multiple_issues(self):
        string = "MY LITTLE PONY FIENDSHIP IS MAGIC #1-5 COMP 5 CVR BOX SET"
        output = previews_parser.parse_release_info(string)
        expected = {}
        self.assertEquals(output, expected)

    def test_ignores_posters(self):
        string = "A-FORCE #1 BY CHEUNG POSTER"
        output = previews_parser.parse_release_info(string)
        self.assertEquals(output, {})

    def test_does_not_ignore_comic_with_poster_in_title(self):
        string = "BATMAN POSTER #2"
        output = previews_parser.parse_release_info(string)
        expected = {
            'series': 'Batman Poster',
            'issue': 2,
        }
        self.assertEquals(output, expected)
