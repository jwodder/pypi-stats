#!/usr/bin/env python3
__requires__ = [
    "click >= 7.0",
    "pypistats ~= 0.12.0",
    "txtble ~= 0.11",
]

from collections import namedtuple
import csv
import json
from operator import attrgetter
import sys
from xmlrpc.client import ServerProxy
import click
import pypistats
from txtble import Txtble

PackageStats = namedtuple("PackageStats", "package last_month last_week last_day")


class CSVFormatter:
    FIELDS = ["package", "last_month", "last_week", "last_day"]

    def __init__(self):
        self.out = csv.DictWriter(sys.stdout, self.FIELDS)

    def __enter__(self):
        self.out.writeheader()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def add_row(self, pstats):
        self.out.writerow({f: getattr(pstats, f) for f in self.FIELDS})


class TableFormatter:
    def __init__(self):
        self.tbl = Txtble(
            headers=["Package", "Last Month", "Last Week", "Last Day"],
            align=["l", "r", "r", "r"],
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print(self.tbl)

    def add_row(self, pstats):
        self.tbl.append(pstats)


@click.command()
@click.option(
    "-A",
    "--sort-alpha",
    "sortby",
    flag_value="name",
    help="Sort packages alphabetically",
)
@click.option(
    "-C",
    "--csv",
    "fmt",
    flag_value=CSVFormatter,
    type=click.UNPROCESSED,
    default=True,
    help="Output CSV [default]",
)
@click.option(
    "-N",
    "--sort-num",
    "sortby",
    flag_value="downloads",
    help="Sort packages by downloads, highest first",
)
@click.option(
    "-T",
    "--table",
    "fmt",
    flag_value=TableFormatter,
    type=click.UNPROCESSED,
    help="Output an ASCII table",
)
@click.option(
    "-u",
    "--user",
    multiple=True,
    help="Show packages belonging to the given PyPI user",
)
@click.argument("package", nargs=-1)
def main(fmt, user, package, sortby):
    """Show downloads stats for PyPI packages"""
    pkgs = iter_packages(user, package)
    if sortby == "name":
        pkgs = sorted(pkgs)
    stats = map(get_package_stats, pkgs)
    if sortby == "downloads":
        stats = sorted(stats, key=attrgetter("last_month"), reverse=True)
    with fmt() as formatter:
        for s in stats:
            formatter.add_row(s)


def iter_packages(users, packages):
    seen = set()
    if users:
        with ServerProxy("https://pypi.org/pypi") as pypi_xml:
            for u in users:
                for _, pkg in pypi_xml.user_packages(u):
                    if pkg not in seen:
                        yield pkg
                        seen.add(pkg)
    for pkg in packages:
        if pkg not in seen:
            yield pkg
            seen.add(pkg)


def get_package_stats(package):
    data = json.loads(pypistats.recent(package, format="json"))
    return PackageStats(
        package=package,
        last_month=data["data"]["last_month"],
        last_week=data["data"]["last_week"],
        last_day=data["data"]["last_day"],
    )


if __name__ == "__main__":
    main()
