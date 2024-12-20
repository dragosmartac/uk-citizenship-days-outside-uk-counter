#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta


def parse_date(date_str: str) -> datetime:
    """
    Parse a date string into a datetime object.
    The function supports two formats:
    - "%d %b %Y" (e.g., "01 Jan 2022")
    - "%d %B %Y" (e.g., "01 January 2022")
    - "%d/%m/%Y" (e.g., "01/01/2022")
    Args:
        date_str (str): The date string to be parsed.
    Returns:
        datetime: A datetime object representing the input date.
    """

    date_str = date_str.strip()
    # https://strftime.org/ cheat sheet for date format
    for fmt in ["%d %b %Y", "%d %B %Y", "%d/%m/%Y"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    # If none of the formats match, raise an error
    raise ValueError(
        f"Invalid date format for {date_str}. Supported formats are 'DD MMM YYYY', 'DD Month YYYY' and 'DD/MM/YYYY."
    )


def parse_dates(filepath: str) -> list[tuple[datetime, datetime]]:
    """
    Parse a file containing date ranges into a list of tuples.
    The file is expected to have one date range per line, with the start and end dates separated by a hyphen.
    Args:
        filepath (str): The path to the file containing the date ranges.
    Returns:
        list[tuple[datetime, datetime]]: A list of tuples, where each tuple contains the start and end dates as datetime objects.
    Raises:
        AssertionError: If a start date is after its corresponding end date.
    """

    with open(filepath, "r") as f:
        lines = f.readlines()

    dates = []
    for line in lines:
        start_date, end_date = line.split("-")
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        assert (
            start_date <= end_date
        ), f"Start date {start_date} is after end date {end_date}"

        dates.append((start_date, end_date))

    return dates


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Script to count the number of days spent outside of the UK as provided in the input file"
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        required=True,
        help="Input file containing the travel dates. See an example in the test file",
    )
    args = parser.parse_args()

    dates = parse_dates(args.file)

    total_days = 0
    total_full_days = 0  # The government website only counts full days

    total_days_past_year = 0
    total_full_days_past_year = 0
    day_one_year_ago = datetime.now() - timedelta(days=365)

    print()
    print("-" * 50)
    print("Computations:")
    print("-" * 50)
    print()

    for start_date, end_date in dates:
        print(f"Start date: {start_date.date()}, end date: {end_date.date()}")
        print(f"Full days spent outside of the UK: {(end_date - start_date).days}")

        total_days += (end_date - start_date).days + 1
        total_full_days += (end_date - start_date).days

        if end_date >= day_one_year_ago:
            total_days_past_year += (
                end_date - max(start_date, day_one_year_ago)
            ).days + 1
            total_full_days_past_year += (
                end_date - max(start_date, day_one_year_ago)
            ).days

    print()
    print("-" * 50)
    print(
        f"Total full days spent outside of the UK: {total_full_days} ({total_days} including travel days)"
    )
    print(
        f"Total full days spent outside of the UK in the past year: {total_full_days_past_year} ({total_days_past_year} including travel days)"
    )
    print("-" * 50)


if __name__ == "__main__":
    main()
