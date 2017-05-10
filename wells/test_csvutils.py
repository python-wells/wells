#!/usr/bin/env python
# coding=utf-8

"""
tests for csvutils
"""

from __future__ import print_function, unicode_literals

from .csvutils import rows_to_csv


def test_rows_to_csv():
    assert rows_to_csv([
        ("abc", u"呵呵", 123),
        ("def", u"哈哈", 456),
    ]) == u"""\
abc,呵呵,123\r
def,哈哈,456\r
"""
