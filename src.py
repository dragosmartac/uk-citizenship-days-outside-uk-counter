#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta


def parse_date(date_str: str) -> datetime:
    date_str = date_str.strip()
    return datetime.strptime(date_str, "%d %b %Y")


def parse_dates(filepath: str) -> list[tuple[datetime, datetime]]:
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
