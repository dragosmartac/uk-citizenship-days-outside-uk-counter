#!/usr/bin/env python3

import unittest

from datetime import datetime

from src import parse_date


class TestScript(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(parse_date("1 Jan 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("01 Jan 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("01 January 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("31 Dec 2023"), datetime(2023, 12, 31))


if __name__ == "__main__":
    unittest.main()
