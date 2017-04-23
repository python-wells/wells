#!/usr/bin/env python
# coding=utf-8

"""
bash script utils.
"""

import re
import shlex


from .py3utils import IS_PY3


SHELL_ASSIGNMENT_PATTERN = re.compile(r'^(?:(export|EXPORT)[ \t]+)?([_a-zA-Z0-9]+)[ \t]*=([ \t]*$|[^ \t]+(.*)$)')    # pylint: disable=line-too-long

# Prior to Python 2.7.3, shlex module did not support Unicode input.
SHLEX_SUPPORT_UNICODE = shlex.split(u"a") == ['a']


def quote_sh_value(value):
    """quote a string value for use in sh config.

    """
    if not value:
        return u''
    value = u"%s" % (value,)
    return u'"%s"' % (value.replace('"', '\"'))


def parse_sh_value(value):
    try:
        if not SHLEX_SUPPORT_UNICODE:
            value = value.encode('utf-8')
        r = shlex.split(value)[0]
        # in python2, split result is always str (bytes).
        if IS_PY3:
            return r
        return r.decode('utf-8')
    except IndexError:
        return u""


def get_var(content, var_name):
    """get var's value from content.

    return u"" if var did not appear to be assigned in content.

    """
    content = content.rstrip()

    for line in content.split('\n'):
        line = line.strip()
        mo = SHELL_ASSIGNMENT_PATTERN.match(line)
        if mo:
            var = mo.group(2)
            current_value = parse_sh_value(mo.group(3))
            if var == var_name:
                return current_value
    return u""


def set_var(content, var_name, value, export=False):
    """set var to value in content.

    The var_name is case sensitive, as in bash.

    To simplify development, this function does not check multiple appearance
    of the same variable.

    A variable should be on its own line in "X=Y" form or in "export X=Y"
    form. All other form is not supported, and result will be undefined.

    Args:
        content: the bash script content
        var_name: variable name
        value: variable's value
        export: if True, when var does not appear in content, add it using
                "export var=value" form.

    Return:
        (updated?, content)
        updated?: True if the content is modified.
        content: the content after setting the variable to given value.

    """
    result = []

    value = u"%s" % (value,)
    content = content.rstrip()

    i = iter(content.split('\n'))
    while True:
        try:
            line = next(i)
        except StopIteration:
            # var is not found in content
            result.append(u"%s%s=%s" % (
                u"export " if export else u"",
                var_name, quote_sh_value(value)))
            return True, u'\n'.join(result) + u'\n'
        line = line.strip()
        mo = SHELL_ASSIGNMENT_PATTERN.match(line)
        if mo:
            matched_export = mo.group(1)
            var = mo.group(2)
            current_value = parse_sh_value(mo.group(3))
            if var == var_name:
                if current_value == value:
                    return False, content + u'\n'
                result.append(u"%s%s=%s" % (
                    u"export " if matched_export else u"",
                    var_name, quote_sh_value(value)))
                result.extend(i)
                return True, u'\n'.join(result) + u'\n'
            else:
                result.append(line)
        else:
            result.append(line)
