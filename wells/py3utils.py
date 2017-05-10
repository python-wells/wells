#!/usr/bin/env python
# coding=utf-8

"""python 3 portability issue helper.

"""

# pylint: disable=unused-import

import sys


IS_PY2 = sys.version_info[0] == 2
IS_PY3 = sys.version_info[0] == 3

try:
    from itertools import izip    # pylint: disable=no-name-in-module
except ImportError:
    izip = zip

try:
    newstr = unicode    # pylint: disable=undefined-variable
except NameError:
    newstr = str


basestring_type = str if IS_PY3 else basestring    # pylint: disable=undefined-variable

if IS_PY2:
    import cStringIO    # pylint: disable=import-error
    BytesIO = cStringIO.StringIO
    StringIO = cStringIO.StringIO
else:
    import io
    BytesIO = io.BytesIO
    StringIO = io.StringIO
