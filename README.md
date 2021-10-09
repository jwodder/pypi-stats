`pypi-stats` (note hyphen) is a wrapper around
[`pypistats`](https://github.com/hugovk/pypistats) (note non-hyphen) for making
API requests to <https://pypistats.org> (note .org).  Specifically, it takes
the names of a number of PyPI packages (and/or PyPI users via the `-u`/`--user`
option) and lists the packages' and users' packages' downloads stats for the
last month, week, and day.  By default, it outputs in CSV, but the
`-T`/`--table` option can be used to get an ASCII table.

That's it.  That's all it does.
