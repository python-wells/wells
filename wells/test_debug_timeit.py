#!/usr/bin/env python
# coding=utf-8

import time
import logging

from .debug import timeit

logger = logging.getLogger(__name__)


@timeit
def func1():
    time.sleep(0.02)
    return "abc"


def test_func1():
    try:
        t, result = func1()
        assert t >= 0.02
        assert result == "abc"
    except ValueError:
        assert False, "expect a tuple of 2 elements"


@timeit
def func2():
    time.sleep(0.05)


def test_func2():
    try:
        t, result = func2()    # pylint: disable=assignment-from-no-return
        assert t >= 0.05
        assert result is None
    except ValueError:
        assert False, "expect a tuple of 2 elements"
