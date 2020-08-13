#!/usr/bin/env python3

"""Module for 591 crawler."""

import argparse
import csv
import datetime

import fetcher
import store


def yield_house(house: fetcher.House):
    yield house.post_id
    yield house.region
    yield house.section
    yield house.description
    yield house.price_value
    yield house.area
    yield str(datetime.datetime.fromtimestamp(house.refresh_time))
    yield fetcher.get_591_url(house)


def export(database: str, comma: str):
    storage = store.LiteHouseStore(database)

    csv_file = open(comma, "w", newline="")
    writer = csv.writer(csv_file)

    for key in storage:
        house = storage[key]
        writer.writerow(yield_house(house))


def main() -> None:
    parser = argparse.ArgumentParser(description="Export CSV")
    parser.add_argument("sqlite3", help="The path to sqlite3 file")
    parser.add_argument("csv", help="The output path of CSV file")
    args = vars(parser.parse_args())

    export(args["sqlite3"], args["csv"])


if __name__ == "__main__":
    main()
