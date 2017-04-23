#!/usr/bin/env python
# coding=utf-8

"""redis utilities.

Note: in python3, all redis functions return byte instead of string.

For both key name, string value, set/list/hash, all things involving strings
will be bytes when they are coming from redis server. This module provide some
helper function to help you convert them back to string objects.

"""

from itertools import chain
from .utils import ensure_str


class RedisNamespace(object):    # pylint: disable=too-few-public-methods
    def __init__(self, namespace):
        """create a top level namespace.

        After creating it, use .key() to get a key in this namespace.

        """
        self.namespace = ensure_str(namespace)

    def key(self, *args):
        """build a redis key in this namespace.

        Args:
            Each arg means one level of sub namespace.
            The last arg is the identifying key.
            Each arg could be either string or byte.

        Return:
            a string by combining top level namespace and each args with ":"

        """
        return ":".join(chain((self.namespace,), map(ensure_str, args)))


def ns(*args):
    """build a redis key in given namespace.

    Args:
        each arg will be namespace and key strings or bytes.

    Return:
        a string by combining all args with ":"

    """
    return ":".join(map(ensure_str, args))


def redis_string_to_list(value, sep=','):
    """convert a comma (or sep) separated string to list.

    Args:
        value: byte, a redis string.
        sep: string, which separator is used to separator items

    Return:
        a list of strings. Could be empty list if original string is None or
        empty.

    """
    return value.decode('utf-8').split(sep) if value else []


def redis_hash_to_dict(redis_hash):
    """convert redis hash to python dict.

    Args:
        redis_hash: redis hash object, a dict with all keys and values in byte.

    Return:
        a python dict with all keys and values in string.

    """
    return {k.decode("utf-8"): v.decode("utf-8") if v else ""
            for k, v in redis_hash.items()}


def redis_list_to_list(redis_list):
    """convert redis list to python list.

    This just convert bytes to unicode string.

    """
    return [i.decode('utf-8') for i in redis_list]
