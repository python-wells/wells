#!/usr/bin/env python
# coding=utf-8

"""
test utils.retry decorator
"""

from __future__ import print_function, unicode_literals

from .utils import retry


G1 = 2    # for use with t1()
G2 = 2    # for use with t2()
G3 = 2    # for use with t3()
G5 = 0    # for use with t5()
G6 = 0    # for use with t6()


@retry(interval=0.01)
def t1():
    global G1
    print(G1)
    if G1 < 0:
        return "OK"
    G1 -= 1
    return 1 / 0


@retry(times=2, interval=0)
def t2():
    global G2
    if G2 < 0:
        return "OK"
    G2 -= 1
    return 1 / 0


@retry(interval=[0.01, 0.02, 0.03, 0.04])
def t3():
    global G3
    if G3 < 0:
        return "OK"
    G3 -= 1
    return 1 / 0


@retry(times=5, interval=[0.01, 0.02])
def t4():
    """testing the short interval parameter.

    """
    return 1 / 0


@retry(interval=0)
def t5():
    global G5
    G5 += 1
    return {'ok': False, 'msg': 't5 will always fail'}


@retry(interval=0, error_dict_support=False)
def t6():
    global G6
    G6 += 1
    return {'ok': False, 'msg': 't6 will return on first try'}


def test_retry_decorator():
    assert t1() == "OK"
    try:
        t2()
        assert False, "should throw ZeroDivisionError"
    except ZeroDivisionError:
        pass
    assert t3() == "OK"
    try:
        t4()
        assert False, "should throw ZeroDivisionError"
    except ZeroDivisionError:
        pass
    assert t5() == {'ok': False, 'msg': 't5 will always fail'}
    assert G5 == 4
    assert t6() == {'ok': False, 'msg': 't6 will return on first try'}
    assert G6 == 1
