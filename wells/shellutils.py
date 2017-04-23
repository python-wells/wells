#!/usr/bin/env python
# coding=utf-8

"""
shell utils
"""


import re


shell_safe_pattern = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]*$')


def is_shell_safe(key):
    """return truth if key is a shell safe variable name.

    """
    return shell_safe_pattern.match(key)
