#!/usr/bin/env python2
# coding=utf-8

"""
debug tools
"""

import logging
import time
import functools


logger = logging.getLogger(__name__)


def trace_time(brief=True, threshold=0.02):
    """trace a function's run time.

    This is designed as a decorator creator. To use the decorator, either use
    @trace_time() or @trace_time(brief=False)

    Args:
        brief: if True, the generated decorator does not print args and kwargs
               in log. Beware, some args and kwargs will be long.
        threshold: optional, float. if set, only log a message when time cost
                   is larger than this many seconds.

    Return:
        a decorator which when used, will return what the decorated func
        returns, and with additional log for tracing run time.

    """
    def gen_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                r = func(*args, **kwargs)
                return r
            finally:
                duration = time.time() - start_time
                if (not threshold) or duration >= threshold:
                    if brief:
                        logger.debug(u"trace_time, func=%s, duration=%.2f",
                                     func.__name__, duration)
                    else:
                        logger.debug(u"trace_time, func=%s, args=%s, "
                                     u"kwargs=%s, duration=%.2f",
                                     func.__name__, args, kwargs, duration)
        return wrapper
    return gen_wrapper


def timeit(func):
    """a decorator that returns func runtime in seconds.

    It changes function's return value to be a tuple of:
    (time_cost_in_seconds_as_float, original_return_value)

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _start_time = time.time()
        r = func(*args, **kwargs)
        _end_time = time.time()
        return _end_time - _start_time, r
    return wrapper
