# Unit tests

import unittest
from TurnipTrackerBot import extract_date, parse_args, extract_period, extract_price


class StringParsingTest(unittest.TestCase):

    ##################### PERIOD TESTS #####################
    def test_end_period(self):
        test_string = "$turnip 50 am"
        self.assertEqual(extract_period(test_string), "AM")

    def test_start_period(self):
        test_string = "$turnip pm 50"
        self.assertEqual(extract_period(test_string), "PM")

    def test_date_period(self):
        test_string = "$turnip 50 am 4/20"
        self.assertEqual(extract_period(test_string), "AM")

    def test_date_mid_period(self):
        test_string = "$turnip 50 4/20 am"
        self.assertEqual(extract_period(test_string), "AM")

    def test_double_period(self):
        test_string = "$turnip 50 am pm"
        self.assertEqual(extract_period(test_string), "AM")

    def test_with_user(self):
        test_user = "$turnip 89 am --user AlanWho"
        self.assertEqual(extract_period(test_user), "AM")

    def test_alan_bug(self):
        alan_string = "$turnip am 89"
        self.assertEqual(extract_period(alan_string), "AM")

    ##################### PRICE TESTS #####################
    def test_end_price(self):
        test_string = "$turnip 50 am"
        self.assertEqual(extract_price(test_string), 50)

    def test_start_price(self):
        test_string = "$turnip pm 50"
        self.assertEqual(extract_price(test_string), 50)

    def test_date_price(self):
        test_string = "$turnip 50 am 4/20"
        self.assertEqual(extract_price(test_string), 50)

    def test_date_mid_price(self):
        test_string = "$turnip 50 4/20 am"
        self.assertEqual(extract_price(test_string), 50)

    def test_double_price(self):
        test_string = "$turnip 50 50 pm"
        self.assertEqual(extract_price(test_string), 50)

    def test_Alan_1(self):
        test_string = "$turnip am 1.1"
        self.assertEqual(extract_price(test_string), None)

    def test_Alan_2(self):
        test_string = "$turnip am 1+1"
        self.assertEqual(extract_price(test_string), None)

    def test_Alan_3(self):
        test_string = "$turnip am 1yourmom"
        self.assertEqual(extract_price(test_string), None)

    def test_alan_4(self):
        test_string = "$turnip am 1\\0"
        self.assertEqual(extract_price(test_string), None)

    def test_alan_5(self):
        test_string = "$turnips am 09"
        self.assertEqual(extract_price(test_string), 9)

    def test_alan_6(self):
        test_string = r"$turnips am \n69"
        self.assertEqual(extract_price(test_string), None)

    def test_alan_7(self):
        test_string = "$turnips am:0)"
        self.assertEqual(extract_price(test_string), None)


if __name__ == "__main__":
    unittest.main()
