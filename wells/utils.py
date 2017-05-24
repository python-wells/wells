#!/usr/bin/env python
# coding=utf-8

"""
wells common utils
"""

from __future__ import unicode_literals

import logging
import re
import hashlib
import uuid
import datetime
import time
import functools
import hmac
import json
from itertools import cycle, chain, repeat

from .py3utils import izip, newstr, basestring_type, IS_PY2

logger = logging.getLogger(__name__)


def ok(**kwargs):
    kwargs['ok'] = True
    return kwargs


def error(**kwargs):
    kwargs['ok'] = False
    return kwargs


def fargs(args):
    """format an args tuple to unicode string.

    """
    return u', '.join(newstr(arg) for arg in args)


def ensure_str(byte_or_str):
    """convert a byte or unicode string object to unicode string.

    Useful when dealing with redis return values.

    """
    x = byte_or_str
    return x if isinstance(x, newstr) else x.decode("utf-8")


def ensure_byte(byte_or_str):
    """convert a byte or unicode string object to byte.

    """
    x = byte_or_str
    return x.encode('utf-8') if isinstance(x, newstr) else x


def new_uuid():
    return str(uuid.uuid4())


def is_valid_uuid(text):
    """Return truth if given string is valid uuid.

    Args:
        text: a uuid string

    Return:
        a uuid string in standard format (dash-separated, lowercase) when text
        is valid uuid or False.

    """
    try:
        return str(uuid.UUID(text))
    except ValueError:
        return False


def get_week_number():
    """return current week number.

    """
    return datetime.date.today().isocalendar()[1]


def now():
    """return current datetime in 'YYYY-MM-DD HH:MM:SS' format.

    """
    sep = b' ' if IS_PY2 else ' '
    return datetime.datetime.now().isoformat(sep)[:19]


def today():
    """return today's date in 'YYYY-MM-DD' format.

    """
    return datetime.date.today().isoformat()


def tomorrow():
    """return tomorrow's date in 'YYYY-MM-DD' format.

    """
    today = datetime.date.today()     # pylint: disable=redefined-outer-name
    d = today + datetime.timedelta(days=1)
    return d.isoformat()


def yesterday():
    """return yesterday's date in YYYY-MM-DD format.

    """
    today = datetime.date.today()     # pylint: disable=redefined-outer-name
    d = today - datetime.timedelta(days=1)
    return d.isoformat()


def get_ts_microseconds():
    """return current timestamp in microsecond since Epoch.

    """
    return int(time.time() * 1000000)


def datetime_to_timestamp(d):
    """convert a datetime object to seconds since Epoch.

    Args:
        d: a naive datetime object in default timezone

    Return:
        int, timestamp in seconds

    """
    return int(time.mktime(d.timetuple()))


def datetime_to_timestamp_in_microseconds(d):
    """convert a naive datetime object to microseconds since Epoch.

    """
    return int(time.mktime(d.timetuple()) * 1000000)


def datetime_to_timestamp_in_milliseconds(d):
    """convert a naive datetime object to milliseconds since Epoch.

    """
    return int(time.mktime(d.timetuple()) * 1000)


def timestamp_to_datetime(ts):
    """convert a timestamp (seconds since Epoch) to datetime object.

    Args:
        ts: int, a timestamp in seconds

    Return:
        a naive datetime object in default timezone.

    """
    return datetime.datetime.fromtimestamp(ts)


def format_datetime(datetime_obj, sep="T"):
    """format datetime to "YYYY-MM-DDTHH:MM:SS" format.

    No timezone is supported.

    Args:
        datetime_obj: a datetime object.
        sep: separator to use between date and time. default is "T".

    Return:
        a string in "YYYY-MM-DDTHH:MM:SS" format.

    """
    return datetime_obj.isoformat(sep)[:19]


def seconds(time_duration):
    """convert a human readable time_duration to seconds.

    Args:
        time_duration: like "5", "5s", "10min", "1h", "1d".

    """
    if isinstance(time_duration, (int, float)):
        return int(time_duration)
    if not isinstance(time_duration, basestring_type):
        raise ValueError("seconds() require a string, but found: %s" % (
            time_duration,))
    pattern = re.compile(r"^([0-9]+)(s(?:ec)?|h(?:our)?|d(?:ay)?|m(?:in)?)?$")
    mo = pattern.match(time_duration)
    if mo:
        digits = int(mo.group(1))
        suffix = mo.group(2)
        if suffix:
            suffix = suffix[:1]
        suffix_unit = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 24 * 3600,
            None: 1
        }
        try:
            return digits * suffix_unit[suffix]
        except KeyError:
            raise ValueError("invalid time_duration suffix: %s" % (suffix,))
    raise ValueError("invalid time_duration: %s" % (time_duration,))


def date_to_datetime(d):
    """convert date to datetime.

    """
    return datetime.datetime.combine(d, datetime.datetime.min.time())


def seconds_to_0000():
    """seconds to next 00:00.

    """
    d = datetime.date.today() + datetime.timedelta(days=1)
    now_ = datetime.datetime.now()
    return int((date_to_datetime(d) - now_).total_seconds())


def uniq(iterable):
    """return an iterable that does not have duplicated elements.

    order of elements is reserved.

    """
    seen = set()
    for e in iterable:
        if e not in seen:
            yield e
            seen.add(e)


def flatten(list_of_lists):
    """flatten one level of nesting.

    """
    return chain.from_iterable(list_of_lists)


def group(n, iterable, value_constructor=lambda x: x):
    """group items to iterables of size n.

    the last part can have less than n elements.

    Args:
        n: group by this number
        iterable: any iterable
        value_constructor: usually the return value is an iterable of
                           lists. if you don't want lists, you can pass in a
                           function that converts lists to your target
                           object. This is a function that takes a list and
                           returns a object.

    """
    if n < 1:
        raise ValueError("group by N, N should be at least 1")
    one_element = []
    for index, e in izip(cycle(range(n)), iterable):
        one_element.append(e)
        if index == n - 1:
            yield value_constructor(one_element[:])
            one_element = []
    if one_element:
        yield value_constructor(one_element)


def first(predicate, iterable):
    """return first element in iterable that satisfies given predicate.

    Args:
        predicate: a function that takes one parameter and return a truth value.
        iterable: any iterable, the items to check.

    Return:
        first element in iterable that satisfies predicate, or None if no such
        element.

    """
    for i in iterable:
        if predicate(i):
            return i
    return None


def len_gen(gen):
    """return length of a generator.

    built-in len() does not work on generators.

    Note: like iterators, generators can only iter once, so after running
    len_gen() on it, you can't iter over it again.

    """
    return functools.reduce(lambda x, y: x + 1, gen, 0)


def gen_prefixes(text, min_length=1):
    """return an iterable of prefix strings for given text.

    Args:
        text: the full string.
        min_length: minimum length of prefix. default is 1.

    """
    for i in range(min_length, len(text) + 1):
        yield text[:i]


def drop_prefix(prefix, text):
    """drop prefix from text if it exists.

    Args:
        prefix: the prefix to drop.
        text: the full string.

    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def allow_fail(f):
    """a decorator that wraps a function for safe error handling.

    This decorator capture uncaught exceptions and return an error() result.
    For more advanced composition, consider use the either monad instead.

    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:    # pylint: disable=broad-except
            logger.exception("allow_fail caught exception")
            return error(msg=u"Uncaught Exception: %s: %s" % (
                e.__class__.__name__, e))
    return wrapper


def sha1sum(str_or_byte):
    """return sha1sum for given byte string.

    """
    return hashlib.sha1(ensure_byte(str_or_byte)).hexdigest()


def md5sum(str_or_byte):
    """return md5sum for given byte string.

    """
    return hashlib.md5(ensure_byte(str_or_byte)).hexdigest()


def hmac_sha256(key, msg=None):
    """return hmac object for given key and msg.

    Args:
        key: bytes or string, the HMAC key.
        msg: bytes, the message to calculate HMAC hash.

    Return:
        hmac object. You may call .update() to update it.

    """
    return hmac.new(ensure_byte(key), msg, digestmod=hashlib.sha256)


def hmac_sha256_hex(key, msg):
    """return hmac hexdigest for given key and msg.

    Args:
        key: bytes or string, the HMAC key.
        msg: bytes, the message to calculate HMAC hash.

    Return:
        string, the hexdigest of the HMAC result.

    """
    return hmac_sha256(key, msg).hexdigest()


def wait_until(checker, check_interval=1, max_tries=None):
    """wait until checker returns truth value.

    Args:
        checker: callable, a check function that return True on success.
        check_interval: int, check interval in seconds.
        max_tries: optional, int, how many times to try before returning False.
                   None or -1 means infinity.

    Return:
        checker()'s result if checker() return truth value.

        if checker() never return truth value, this function tries at most
        max_tries times, then return False.

    """
    if max_tries < 0:
        max_tries = None
    tries = 0
    while True:
        r = checker()
        if r:
            return r
        tries += 1
        if max_tries and tries == max_tries:
            return False
        time.sleep(check_interval)


def string_to_list(line, sep=','):
    """convert a comma (or sep) separated string to list.

    If line is None (or any falsy value), return [].

    """
    return line.split(sep) if line else []


def retry(times=3, interval=(1, 5, 10), error_dict_support=True):
    """auto retry when function fails.

    This is designed as a decorator creator. To use the decorator, either use
    @retry() or @retry(times=3, interval=5) or @retry(times=3, interval=[1, 5,
    10])

    A function is considered failed when it raised an unhandled exception.

    Args:
        times: max retry times. so function may run 1 + times in worst case.
        interval: if set to an int/float, means retry after these many seconds.
                  if set to an iterable, means retry interval for each retry;
                  if interval iterable is shorter than times, the last value
                  will be used for remaining retries.
                  default interval is (1, 5, 10).
        error_dict_support: if True when function return a dict with
                            {'ok': False}, treat it as failure.

    Return:
        a decorator which when used, will return what the decorated func
        returns, but with auto retry support.

    """
    def gen_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retry_time = 0
            if isinstance(interval, (int, float)):
                interval_iter = repeat(interval)
            else:
                interval_iter = iter(interval)
            while True:
                try:
                    r = func(*args, **kwargs)
                    if error_dict_support and retry_time < times:
                        if isinstance(r, dict) and 'ok' in r:
                            if not r['ok']:
                                raise RuntimeError(r.get('msg', ''))
                    return r
                except Exception as _:    # pylint: disable=broad-except
                    if retry_time >= times:
                        logger.error("max retry reached, func=%s, retry=%s",
                                     func.__name__, retry_time)
                        raise
                    else:
                        logger.exception(
                            "will retry because function raised exception")
                        try:
                            seconds = next(interval_iter)  # pylint: disable=redefined-outer-name
                        except StopIteration:
                            interval_iter = repeat(seconds)
                        time.sleep(seconds)
                        retry_time += 1
                        logger.debug("sleeping %s before auto retry", seconds)
                        logger.info(
                            "auto retry, func=%s, retry=%s, last_sleep=%s",
                            func.__name__, retry_time, seconds)
        return wrapper
    return gen_wrapper


def check(func):
    """make function a sanity checker.

    This is a decorator that wraps a function into a sanity checker.
    A sanity checker prints output like this when run:

    check_db ... pass
    check_redis ... failed.
    xxx exception or error
    check_celery ... pass

    run xx checks, xx passed, xx failed.
    exit code will be 0 when all checks pass.

    The original function should return truthy value when check passes, return
    falsy value or raise exception when check fails.

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
            logger.info("%s ... %s", func.__name__,
                        "pass" if r else "failed")
            return r
        except Exception as _:    # pylint: disable=broad-except
            logger.exception("%s ... %s", func.__name__, "failed")
    return wrapper


class BetterJsonEncoder(json.JSONEncoder):
    """why python's built-in json encoder doesn't support date/datetime?

    This is a replacement that support those data types.

    """
    def default(self, o):    # pylint: disable=method-hidden
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def to_json(obj, cls=BetterJsonEncoder, **kwargs):
    """convert python object to json string.

    This function supports date and datetime objects.
    If you have custom class, try subclass BetterJsonEncoder and use
    json.dumps(obj, cls=YourJsonEncoder) instead.

    Args:
        obj: any python object
        cls, **kwargs: the same kwargs accepted by json.dumps()

    Return:
        a string in json format. This may raise TypeError if object is not
        JSON serializable

    """
    return json.dumps(obj, cls=cls, **kwargs)
