#!/usr/bin/env python
# coding=utf-8

"""
param check utils
"""

from __future__ import print_function, unicode_literals

from .utils import ok, error
from .py3utils import basestring_type


def check_required_params(keys, dict_obj):
    """check whether given keys exists and is not empty in dict_obj.

    Args:
        keys: an iterable of keys to check.
        dict_obj: a python dict object containing the params to check.

    Return:
        ok() if all keys exists and is not empty.
        error(msg="") if some keys are missing or value is empty (empty
                      string or None).

    """
    msgs = []
    for k in keys:
        if k not in dict_obj:
            msgs.append("missing param: %s" % (k,))
        elif dict_obj[k] in ("", None):
            msgs.append("param \"%s\" is empty" % (k,))
    if msgs:
        return error(msg=", ".join(msgs))
    return ok()


def check_param_type(keys, dict_obj, type_, type_name=None):
    """check whether given keys exists and is of given type_ in dict_obj.

    Args:
        keys: an iterable of keys to check.
        dict_obj: a python dict object containing the params to check.

    Return:
        ok() if all keys exists and is not empty.
        error(msg="") if some keys are missing or value is not of given type_.

    """
    if type_name is None:
        type_name = type_.__name__
    msgs = []
    for k in keys:
        if k not in dict_obj:
            msgs.append("missing param: %s" % (k,))
        elif not isinstance(dict_obj[k], type_):
            msgs.append("param \"%s\" should be a %s, found %s" % (
                k, type_name, dict_obj[k]))
    if msgs:
        return error(msg=", ".join(msgs))
    return ok()


def check_string_params(keys, dict_obj):
    """check whether given keys exists and is a string in dict_obj.

    Args:
        keys: an iterable of keys to check.
        dict_obj: a python dict object containing the params to check.

    Return:
        ok() if all keys exists and is not empty.
        error(msg="") if some keys are missing or value is not string.

    """
    return check_param_type(keys, dict_obj, basestring_type, "string")


def check_int_params(keys, dict_obj):
    """check whether given keys exists and is an int in dict_obj.

    Args:
        keys: an iterable of keys to check.
        dict_obj: a python dict object containing the params to check.

    Return:
        ok() if all keys exists and is not empty.
        error(msg="") if some keys are missing or value is not an int.

    """
    return check_param_type(keys, dict_obj, int)
