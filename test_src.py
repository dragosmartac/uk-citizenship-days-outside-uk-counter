#!/usr/bin/env python3

import unittest

from datetime import datetime
from unittest.mock import patch

from src import (
    compute_travel_logs,
    get_past_year_dates,
    parse_date,
    parse_dates,
    TravelLog,
)


class TestScript(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(parse_date("1 Jan 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("01 Jan 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("01 January 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("1 January 2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("01/01/2023"), datetime(2023, 1, 1))
        self.assertEqual(parse_date("31 Dec 2023"), datetime(2023, 12, 31))

    @patch("builtins.open")
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

    def test_compute_days_summary(self):
        actual_travel_logs = compute_travel_logs(
            [
                (
                    datetime(2023, 11, 1),  # start
                    datetime(2023, 11, 1),  # end
                ),
                (
                    datetime(2023, 11, 2),  # start
                    datetime(2023, 11, 3),  # end
                ),
                (
                    datetime(2023, 11, 5),  # start
                    datetime(2023, 11, 7),  # end
                ),
                (
                    datetime(2023, 11, 7),  # start
                    datetime(2023, 11, 14),  # end
                ),
                (
                    datetime(2024, 12, 27),  # start
                    datetime(2025, 1, 12),  # end
                ),
            ]
        )

        expected_travel_logs = [
            TravelLog(
                start_date=datetime(2023, 11, 1),
                end_date=datetime(2023, 11, 1),
                total_days_outside=1,
                full_days_outside=0,
            ),
            TravelLog(
                start_date=datetime(2023, 11, 2),
                end_date=datetime(2023, 11, 3),
                total_days_outside=2,
                full_days_outside=0,
            ),
            TravelLog(
                start_date=datetime(2023, 11, 5),
                end_date=datetime(2023, 11, 7),
                total_days_outside=3,
                full_days_outside=1,
            ),
            TravelLog(
                start_date=datetime(2023, 11, 7),
                end_date=datetime(2023, 11, 14),
                total_days_outside=8,
                full_days_outside=6,
            ),
            TravelLog(
                start_date=datetime(2024, 12, 27),
                end_date=datetime(2025, 1, 12),
                total_days_outside=17,
                full_days_outside=15,
            ),
        ]

        self.assertEqual(actual_travel_logs, expected_travel_logs)

    @patch("src.datetime")
    def test_get_past_year_dates(self, mock_datetime):
        mock_datetime.today.return_value = datetime(2025, 12, 28)
        dates = [
            (
                datetime(2023, 11, 1),  # start
                datetime(2023, 11, 1),  # end
            ),
            (
                datetime(2023, 11, 2),  # start
                datetime(2023, 11, 3),  # end
            ),
            (
                datetime(2023, 11, 5),  # start
                datetime(2023, 11, 7),  # end
            ),
            (
                datetime(2023, 11, 7),  # start
                datetime(2023, 11, 14),  # end
            ),
            (
                datetime(2024, 12, 27),  # start
                datetime(2025, 1, 12),  # end
            ),
        ]

        expected_past_year_dates = [
            (
                datetime(2024, 12, 28),  # start
                datetime(2025, 1, 12),  # end
            ),
        ]

        self.assertEqual(get_past_year_dates(dates), expected_past_year_dates)


if __name__ == "__main__":
    unittest.main()
