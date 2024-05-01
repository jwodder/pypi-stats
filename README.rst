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
for making API requests to <https://pypistats.org> (note .org).  Specifically,
it takes the names of a number of PyPI packages (and/or PyPI users via the
``-u``/``--user`` option) and lists the packages' and users' packages'
downloads stats for the last month, week, and day.  By default, it outputs in
CSV, but the ``-T``/``--table`` option can be used to get an ASCII table.

That's it.  That's all it does.

.. _pypistats: https://github.com/hugovk/pypistats
