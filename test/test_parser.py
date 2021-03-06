import unittest
import previews_parser

class PreviewsParserTest(unittest.TestCase):
    def test_simple_parsing(self):
        string = "DC COMICS\nJAN150263 AQUAMAN AND THE OTHERS #11 $2.99"
        output = previews_parser.parse(string)
        expected = [
            {
                'series': 'Aquaman And The Others',
                'issue_number': 11,
                'code': 'JAN150263',
                'price': 299,
                'publisher': 'DC Comics',
                'mature': False,
                'printing': 1,
            }
        ]
        self.assertEquals(output, expected)

    def test_multiple_releases(self):
        string = "DC COMICS\nJAN150263 AQUAMAN AND THE OTHERS #11 $2.99\nJAN150300  BATMAN ETERNAL #48  $2.99"
        output = previews_parser.parse(string)
        expected = [
            {
                'series': 'Aquaman And The Others',
                'issue_number': 11,
                'code': 'JAN150263',
                'price': 299,
                'publisher': 'DC Comics',
                'mature': False,
                'printing': 1,
            },
            {
                'series': 'Batman Eternal',
                'issue_number': 48,
                'code': 'JAN150300',
                'price': 299,
                'publisher': 'DC Comics',
                'mature': False,
                'printing': 1,
            },
        ]
        self.assertEquals(output, expected)

    def test_multiple_publishers(self):
        string = "DARK HORSE COMICS\nJAN150087   ANGEL AND FAITH SEASON 10 #12 MAIN CVR  $3.50\n"
        string += "IDW PUBLISHING\nDEC140557   STAR TREK PLANET OF THE APES #3     $3.99"
        output = previews_parser.parse(string)
        expected = [
            {
                'series': 'Angel And Faith Season 10',
                'issue_number': 12,
                'code': 'JAN150087',
                'price': 350,
                'publisher': 'Dark Horse Comics',
                'mature': False,
                'printing': 1,
            },
            {
                'series': 'Star Trek Planet Of The Apes',
                'issue_number': 3,
                'code': 'DEC140557',
                'price': 399,
                'publisher': 'IDW Publishing',
                'mature': False,
                'printing': 1,
            }
        ]
        self.assertEquals(output, expected)

    def test_bad_publisher(self):
        string = 'MARVEL COMICS\nJAN150761  ALL NEW HAWKEYE #1  $3.99\n'
        string += 'COMICS & GRAPHIC NOVELS\nNOV141143   AMAZING WORLD OF GUMBALL #8     $3.99'
        output = previews_parser.parse(string)
        expected = [
            {
                'series': 'All New Hawkeye',
                'issue_number': 1,
                'code': 'JAN150761',
                'price': 399,
                'publisher': 'Marvel Comics',
                'mature': False,
                'printing': 1,
            }
        ]
        self.assertEquals(output, expected)

    def test_duplicate_covers(self):
        string = 'IMAGE COMICS\nJAN150671   BLACK SCIENCE #12 CVR A SCALERA & DINISIO (MR)  $3.50\n'
        string += 'JAN150672    BLACK SCIENCE #12 CVR B MURPHY & HOLLINGSWORTH (MR)     $3.50'
        output = previews_parser.parse(string)
        expected = [
            {
                'series': 'Black Science',
                'issue_number': 12,
                'code': 'JAN150671',
                'price': 350,
                'publisher': 'Image Comics',
                'mature': True,
                'printing': 1,
            }
        ]
        self.assertEquals(output, expected)

    def test_empty_strings(self):
        string = 'IMAGE COMICS\n\nJAN150671   BLACK SCIENCE #12 CVR A SCALERA & DINISIO (MR)  $3.50\n'
        output = previews_parser.parse(string)
        expected = [
            {
                'series': 'Black Science',
                'issue_number': 12,
                'code': 'JAN150671',
                'price': 350,
                'publisher': 'Image Comics',
                'mature': True,
                'printing': 1,
            }
        ]
        self.assertEquals(output, expected)

    def test_non_comic_releases(self):
        string = 'DARK HORSE COMICS\nNOV140012     CONAN HC VOL 17 SHADOWS OVER KUSH   $24.99'
        output = previews_parser.parse(string)
        self.assertEquals(output, [])

    def test_gibberish(self):
        string = "blahblah1234567"
        output = previews_parser.parse(string)
        self.assertEquals(output, [])

    def test_no_newlines(self):
        string = "DC COMICS JAN150263 AQUAMAN AND THE OTHERS #11 $2.99"
        output = previews_parser.parse(string)
        self.assertEquals(output, [])

    def test_pi_in_middle(self):
        string = "DARK HORSE COMICS\nJAN150087   ANGEL AND FAITH SEASON 10 #12 MAIN CVR  $3.50\n"
        string += "IDW PUBLISHING\nDEC140557   STAR TREK PLANET OF THE APES #3     PI\n"
        string += "DC COMICS\nJAN150263 AQUAMAN AND THE OTHERS #11 $2.99"
        output = previews_parser.parse(string)
        expected = [
            {
                'series': 'Angel And Faith Season 10',
                'issue_number': 12,
                'code': 'JAN150087',
                'price': 350,
                'publisher': 'Dark Horse Comics',
                'mature': False,
                'printing': 1,
            },
            {
                'series': 'Aquaman And The Others',
                'issue_number': 11,
                'code': 'JAN150263',
                'price': 299,
                'publisher': 'DC Comics',
                'mature': False,
                'printing': 1,
            },
        ]
        self.assertEquals(output, expected)
