|repostatus| |ci-status| |license|

.. |repostatus| image:: https://www.repostatus.org/badges/latest/concept.svg
    :target: https://www.repostatus.org/#concept
    :alt: Project Status: Concept – Minimal or no implementation has been done
          yet, or the repository is only intended to be a limited example,
          demo, or proof-of-concept.

.. |ci-status| image:: https://github.com/jwodder/pypi-stats/actions/workflows/test.yml/badge.svg
    :target: https://github.com/jwodder/pypi-stats/actions/workflows/test.yml
    :alt: CI Status

.. |license| image:: https://img.shields.io/github/license/jwodder/pypi-stats.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/pypi-stats>`_
| `Issues <https://github.com/jwodder/pypi-stats/issues>`_

``pypi-stats`` (note hyphen) is a wrapper around pypistats_ (note non-hyphen)
for making API requests to https://pypistats.org (note .org) to fetch recent
download stats for given PyPI packages (and/or packages belonging to given PyPI
users), outputting either a CSV file or an ASCII table.

.. _pypistats: https://github.com/hugovk/pypistats


Installation
============
``pypi-stats`` requires Python 3.11 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install it::

    python3 -m pip install git+https://github.com/jwodder/pypi-stats.git


Usage
=====

::

    pypi-stats [<options>] <package> ...

``pypi-stats`` queries https://pypistats.org for the recent download stats for
each PyPI package named on the command line, outputting the number of downloads
for each one in the last month, week, and day.


Options
-------

-A, --sort-alpha                Sort packages alphabetically by name

-C, --csv                       Output a CSV document; this is the default.
                                The first line of the output is a header
                                giving the field names: ``package``,
                                ``last_month``, ``last_week``, and
                                ``last_day``, in that order.

-N, --sort-num                  Sort packages by downloads in the last month in
                                descending order

-T, --table                     Output an ASCII table

-u, --user USER                 Also fetch download stats for all packages for
                                which the given PyPI user is an owner or
                                maintainer.  This option can be specified
                                multiple times.
