#!/usr/bin/env python3

import unittest

from datetime import datetime
from unittest.mock import mock_open, patch

from src import parse_date, parse_dates


class TestScript(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(parse_date("1 Jan 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("01 Jan 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("01 January 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("1 January 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("01/01/2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("31 Dec 2023"), datetime(2023, 12, 31))

    @patch("builtins.open", new_callable=mock_open)
    def test_parse_dates(self, mock_file):
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            "1 Nov 2023 - 31/12/2023\n",
            "02 Feb 2024-28 March 2024\n",
            "01 Jan 2025 -   01/01/2025\n",
        ]

        self.assertEqual(
            parse_dates("some_file.txt"),
            [
                (
                    datetime(2023, 11, 1),  # start
                    datetime(2023, 12, 31),  # end
                ),
                (
                    datetime(2024, 2, 2),  # start
                    datetime(2024, 3, 28),  # end
                ),
                (
                    datetime(2025, 1, 1),  # start
                    datetime(2025, 1, 1),  # end
                ),
            ],
        )

        # Test reversed order fails (not supported)
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            "31/12/2023 - 1 Nov 2023\n",
        ]
        self.assertRaises(AssertionError, parse_dates, "some_file.txt")


if __name__ == "__main__":
    unittest.main()
