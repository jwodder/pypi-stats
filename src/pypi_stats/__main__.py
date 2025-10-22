from __future__ import annotations
import argparse
from collections.abc import Iterable, Iterator, Sequence
import csv
from dataclasses import asdict, astuple, dataclass
from operator import attrgetter
import sys
from types import TracebackType
from typing import Protocol, Self
from xmlrpc.client import ServerProxy
import pypistats
from txtble import Txtble
from . import __version__


@dataclass
class PackageStats:
    package: str
    last_month: int
    last_week: int
    last_day: int


class Formatter(Protocol):
    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None: ...

    def add_row(self, pstats: PackageStats) -> None: ...


class CSVFormatter:
    FIELDS = ["package", "last_month", "last_week", "last_day"]

    def __init__(self) -> None:
        self.out = csv.DictWriter(sys.stdout, self.FIELDS)

    def __enter__(self) -> Self:
        self.out.writeheader()
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        return None

    def add_row(self, pstats: PackageStats) -> None:
        self.out.writerow(asdict(pstats))


class TableFormatter:
    def __init__(self) -> None:
        self.tbl = Txtble(
            headers=["Package", "Last Month", "Last Week", "Last Day"],
            align=["l", "r", "r", "r"],
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is None:
            print(self.tbl)

    def add_row(self, pstats: PackageStats) -> None:
        self.tbl.append(astuple(pstats))


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Show download stats for PyPI packages.\n"
            "\n"
            "`pypi-stats` queries https://pypistats.org for the recent download\n"
            "stats for each PyPI package named on the command line, outputting\n"
            "the number of downloads for each one in the last month, week, and\n"
            "day.\n"
            "\n"
            "Visit <https://github.com/jwodder/pypi-stats> for more information.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-A",
        "--sort-alpha",
        dest="sortby",
        action="store_const",
        const="name",
        help="Sort packages alphabetically by name",
    )
    parser.add_argument(
        "-C",
        "--csv",
        dest="fmt",
        action="store_const",
        const=CSVFormatter,
        default=CSVFormatter,
        help="Output CSV [default]",
    )
    parser.add_argument(
        "-N",
        "--sort-num",
        dest="sortby",
        action="store_const",
        const="downloads",
        help="Sort packages by downloads, highest first",
    )
    parser.add_argument(
        "-T",
        "--table",
        dest="fmt",
        action="store_const",
        const=TableFormatter,
        help="Output an ASCII table",
    )
    parser.add_argument(
        "-u",
        "--user",
        dest="users",
        action="append",
        help="Get stats for packages owned or maintained by the given PyPI user",
        metavar="USER",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument("package", nargs="*")
    args = parser.parse_args()
    pkgs: Iterable[str] = iter_packages(args.users, args.package)
    if args.sortby == "name":
        pkgs = sorted(pkgs)
    stats: Iterable[PackageStats] = map(get_package_stats, pkgs)
    if args.sortby == "downloads":
        stats = sorted(stats, key=attrgetter("last_month"), reverse=True)
    with args.fmt() as formatter:
        for s in stats:
            formatter.add_row(s)


def iter_packages(users: Sequence[str], packages: Sequence[str]) -> Iterator[str]:
    seen = set()
    if users:
        with ServerProxy("https://pypi.org/pypi") as pypi_xml:
            for u in users:
                res = pypi_xml.user_packages(u)
                assert isinstance(res, list)
                for r in res:
                    assert isinstance(r, list)
                    pkg = r[1]
                    assert isinstance(pkg, str)
                    if pkg not in seen:
                        yield pkg
                        seen.add(pkg)
    for p in packages:
        if p not in seen:
            yield p
            seen.add(p)


def get_package_stats(package: str) -> PackageStats:
    data = pypistats.recent(package, format=None)
    return PackageStats(
        package=package,
        last_month=data["last_month"],
        last_week=data["last_week"],
        last_day=data["last_day"],
    )


if __name__ == "__main__":
    main()
