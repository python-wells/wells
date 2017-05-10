#!/usr/bin/env python
# coding=utf-8

"""
file utils
"""

import os
import os.path

from .utils import ok, error


def create_dir_maybe(dir_, mode=None):
    """create dir if it doesn't exist.

    This may raise IOError when dir can not be created.

    """
    if not os.path.exists(dir_):
        os.makedirs(dir_, mode)


def safe_read_file(fn, decode=True):
    """read a file safely.

    Args:
        fn: the filename
        decode: when True, result will be decoded from utf-8 to unicode.

    Return:
        ok(content=content) on success,
        error(msg=error_msg) on failure.

    """
    try:
        with open(fn, 'rb') as f:
            text_bytes = f.read()
            content = text_bytes.decode("utf-8") if decode else text_bytes
        return ok(content=content)
    except EnvironmentError as e:
        return error(msg=u"%s: %s" % (e.__class__.__name__, e))


def safe_write_file(fn, content, encode=True):
    """write content to file safely.

    This function will try to create the parent dirs needed for writing the
    file automatically.

    Args:
        fn: the filename
        content: the content to write to file
        encode: if True encode content to utf-8 before writing it.

    Return:
        ok() on success,
        error(msg="") on failure.

    """
    try:
        d = os.path.dirname(fn)
        if not os.path.exists(d):
            os.makedirs(d)
        with open(fn, 'wb') as f:
            f.write(content.encode('utf-8') if encode else content)
        return ok()
    except EnvironmentError as e:
        return error(msg=u'Error writing to %s: %s' % (fn, e.args))
