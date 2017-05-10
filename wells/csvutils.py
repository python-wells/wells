#!/usr/bin/env python
# coding=utf-8

"""
csv utils
"""

from __future__ import print_function, unicode_literals

import csv

from .py3utils import IS_PY2, newstr, BytesIO, StringIO


def _rows_to_csv_py2(rows):
    """convert rows to csv text.

    Args:
        rows: an iterable of rows to write to csv

    Return:
        unicode string, the csv text

    """
    def str_to_utf8(value):
        """if value is a string, convert it to utf8 bytes.

        """
        if isinstance(value, newstr):
            return value.encode("utf-8")
        return value

    f = BytesIO()
    w = csv.writer(f)
    for row in rows:
        w.writerow([str_to_utf8(x) for x in row])
    return f.getvalue().decode("utf-8")


def _rows_to_csv_py3(rows):
    """convert rows to csv text.

    Args:
        rows: an iterable of rows to write to csv

    Return:
        unicode string, the csv text

    """
    f = StringIO()
    w = csv.writer(f)
    w.writerows(rows)
    return f.getvalue()


if IS_PY2:
    rows_to_csv = _rows_to_csv_py2
else:
    rows_to_csv = _rows_to_csv_py3
