#!/usr/bin/env python
# coding=utf-8

from .bashscript_utils import (parse_sh_value, quote_sh_value,
                               set_var, get_var)


# test for quote_sh_value
def test_quote_sh_value():
    assert quote_sh_value(u"") == u''
    assert quote_sh_value(u"abc") == u'"abc"'
    assert quote_sh_value(u"abc def") == u'"abc def"'
    assert quote_sh_value(u"ab'c") == u"\"ab'c\""
    assert quote_sh_value(u"ab\"c") == u'"ab\"c"'


# test for parse_sh_value
def test_parse_sh_value():
    assert parse_sh_value(u"abc") == u"abc"
    assert parse_sh_value(u"") == u""
    assert parse_sh_value(u'"abc"') == u"abc"
    assert parse_sh_value(u"'abc'") == u"abc"


# test for get_var
def test_get_var():
    assert get_var(u"""\
x=1
y=2
a=b
z=3
""", "x") == u'1'
    assert get_var(u"""\
x=1
y=2
export a=b
z=3
""", "a") == u'b'
    assert get_var(u"""\
x=1
y=2
export a='b'
z=3
""", "a") == u'b'
    assert get_var(u"""\
x=1
y=2
export a="b"
z=3
""", "a") == u'b'
    assert get_var(u"""\
x=1
y=2
export a=b
z=3
""", "foo") == u''


# test for set_var
def test_set_var():
    assert set_var(u"""\
x=1
y=2
a=b
z=3
""", "a", 123) == (True, u"""\
x=1
y=2
a="123"
z=3
""")
    assert set_var(u"""\
a=123
""", "a", 123) == (False, u"""\
a=123
""")
    assert set_var(u"""\
export a=123
x=5
""", "a", 123) == (False, u"""\
export a=123
x=5
""")
    assert set_var(u"""\
y=1
export a=b
""", "a", 123) == (True, u"""\
y=1
export a="123"
""")
    assert set_var(u"""\
y=1
export a=b
""", "a", "") == (True, u"""\
y=1
export a=
""")


# test for set_var
def test_set_var_var_not_found():
    assert set_var(u"""\
x=1
y=2
""", "a", "") == (True, u"""\
x=1
y=2
a=
""")
    assert set_var(u"""\
x=1
y=2
""", "a", "foo", export=True) == (True, u"""\
x=1
y=2
export a="foo"
""")
    assert set_var(u"""\
x=1
y=2
# a=foo
""", "a", "foo", export=True) == (True, u"""\
x=1
y=2
# a=foo
export a="foo"
""")
    assert set_var(u"""\
x=1
y=2
# this line is not a valid assignment, ignored by set_var.
a= foo
""", "a", "foo") == (True, u"""\
x=1
y=2
# this line is not a valid assignment, ignored by set_var.
a= foo
a="foo"
""")


# test for set_var
def test_set_var_case_sensitive():
    assert set_var(u"""\
y=1
a=2
A=3
""", "A", "") == (True, u"""\
y=1
a=2
A=
""")
    assert set_var(u"""\
y=1
export a=b
""", "A", "") == (True, u"""\
y=1
export a=b
A=
""")
    assert set_var(u"""\
y=1
export a=b
""", "A", "foo", export=True) == (True, u"""\
y=1
export a=b
export A="foo"
""")
