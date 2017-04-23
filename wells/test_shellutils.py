#!/usr/bin/env python
# coding=utf-8

from .shellutils import is_shell_safe


# test for is_shell_safe
def test_is_shell_safe():
    assert not is_shell_safe("")
    assert is_shell_safe("a")
    assert is_shell_safe("A")
    assert is_shell_safe("_")
    assert is_shell_safe("a_")
    assert is_shell_safe("foo")
    assert is_shell_safe("Foo")
    assert is_shell_safe("FOO")
    assert is_shell_safe("FOO_BAR")
    assert not is_shell_safe("FOO_ BAR")
    assert not is_shell_safe("FOO.BAR")
    assert not is_shell_safe("6")
    assert not is_shell_safe("6a")
    assert is_shell_safe("a6")
