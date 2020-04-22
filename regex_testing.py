# Unit tests

import unittest
from TurnipTrackerBot import extract_date, extract_flags, extract_period, extract_price

class StringParsingTest(unittest.TestCase):

    def test_period(self):
        test_string = "$turnip 50 am"
        self.assertEqual(extract_period(test_string), "AM")
        

if __name__ == '__main__':
    unittest.main()        