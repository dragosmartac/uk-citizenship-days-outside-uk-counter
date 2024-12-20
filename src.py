#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
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


@dataclass
class TravelLog:
    start_date: datetime
    end_date: datetime
    total_days_outside: int
    full_days_outside: int


def compute_travel_logs(dates: list[tuple[datetime, datetime]]) -> list[TravelLog]:
    return sorted(
        [
            TravelLog(
                start_date=start_date,
                end_date=end_date,
                total_days_outside=(end_date - start_date).days + 1,
                full_days_outside=max(0, (end_date - start_date).days - 1),
            )
            for start_date, end_date in dates
        ],
        key=lambda x: x.start_date,
    )


def get_past_year_dates(
    dates: list[tuple[datetime, datetime]]
) -> list[tuple[datetime, datetime]]:
    today = datetime.today()
    one_year_ago = today - timedelta(days=365)
    return [
        (max(start_date, one_year_ago), end_date)
        for start_date, end_date in dates
        if end_date >= one_year_ago
    ]


def tabulate(table: list[list[str]], headers=list[str]) -> None:
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print(
            "| "
            + " | ".join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line))
            + " |"
        )


def pretty_printer(travel_log: list[TravelLog]):
    print("===========" * 5)
    print()
    table = [
        [
            travel_log.start_date.strftime("%d %b %Y"),
            travel_log.end_date.strftime("%d %b %Y"),
            travel_log.total_days_outside,
            travel_log.full_days_outside,
        ]
        for travel_log in travel_log
    ]
    headers = [
        "Start Date",
        "End Date",
        "Total Days Outside UK",
        "Full Days Outside UK",
    ]
    table = [headers] + table

    col_width = [max(len(str(x)) for x in col) for col in zip(*table)]
    for line in table:
        print(
            "| "
            + " | ".join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line))
            + " |"
        )

    print()
    print(
        f"Total Days Outside UK: {sum(travel_log.total_days_outside for travel_log in travel_log)}"
    )
    print(
        f"Full Days Outside UK: {sum(travel_log.full_days_outside for travel_log in travel_log)}"
    )
    print()
    print("===========" * 5)
    print()


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
    travel_logs = compute_travel_logs(dates)
    travel_logs_past_year = compute_travel_logs(get_past_year_dates(dates))

    print("ALL DATES:")
    pretty_printer(travel_logs)

    print("PAST YEAR DATES:")
    pretty_printer(travel_logs_past_year)


if __name__ == "__main__":
    main()
