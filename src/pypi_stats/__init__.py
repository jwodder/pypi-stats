"""
Show download stats for PyPI packages

Visit <https://github.com/jwodder/pypi-stats> for more information.
"""

from __future__ import annotations
from collections.abc import Callable, Iterable, Iterator, Sequence
import csv
from dataclasses import asdict, astuple, dataclass
import json
from operator import attrgetter
import sys
from types import TracebackType
from typing import Protocol, Self
from xmlrpc.client import ServerProxy
import click
import pypistats
from txtble import Txtble

__version__ = "0.1.0.dev1"
__author__ = "John Thorvald Wodder II"
__author_email__ = "pypi-stats@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/pypi-stats"


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


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
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
@click.version_option(
    __version__,
    "-V",
    "--version",
    message="%(prog)s %(version)s",
)
@click.argument("package", nargs=-1)
def main(
    fmt: Callable[[], Formatter],
    user: tuple[str, ...],
    package: tuple[str, ...],
    sortby: str,
) -> None:
    """Show download stats for PyPI packages"""
    pkgs: Iterable[str] = iter_packages(user, package)
    if sortby == "name":
        pkgs = sorted(pkgs)
    stats: Iterable[PackageStats] = map(get_package_stats, pkgs)
    if sortby == "downloads":
        stats = sorted(stats, key=attrgetter("last_month"), reverse=True)
    with fmt() as formatter:
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
                    pkg = res[1]
                    assert isinstance(pkg, str)
                    if pkg not in seen:
                        yield pkg
                        seen.add(pkg)
    for p in packages:
        if p not in seen:
            yield p
            seen.add(p)


def get_package_stats(package: str) -> PackageStats:
    data = json.loads(pypistats.recent(package, format="json"))
    return PackageStats(
        package=package,
        last_month=data["data"]["last_month"],
        last_week=data["data"]["last_week"],
        last_day=data["data"]["last_day"],
    )


if __name__ == "__main__":
    main()
