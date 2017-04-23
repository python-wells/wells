#!/usr/bin/env python
# coding=utf-8

import time
import logging

from .debug import trace_time

logger = logging.getLogger(__name__)


@trace_time()
def i_will_throw_exception():
    return {}["abc"]


@trace_time(brief=False)
def add_a_b_and_foo(a, b, **kwargs):
    time.sleep(0.1)
    return a + b + kwargs.get("foo", 0)


@trace_time(threshold=None)
def some_quick_calc():
    time.sleep(0.01)
    return 1


@trace_time()
def some_quick_calc2():
    time.sleep(0.01)
    return 1


def test_trace_time():
    try:
        i_will_throw_exception()
        assert False
    except KeyError as _:
        pass

    assert add_a_b_and_foo(1, 2, foo=3) == 6
    assert add_a_b_and_foo(1, 2) == 3
    assert some_quick_calc() == 1
    assert some_quick_calc2() == 1


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG)
    test_trace_time()


if __name__ == '__main__':
    main()
