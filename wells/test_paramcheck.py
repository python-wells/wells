#!/usr/bin/env python
# coding=utf-8

"""
tests for paramcheck module
"""

from __future__ import print_function, unicode_literals

from .paramcheck import check_required_params
from .paramcheck import check_string_params
from .paramcheck import check_int_params


def test_check_required_params():
    params = {}
    r = check_required_params(["id"], params)
    assert not r['ok']
    assert "missing param: id" in r['msg']

    params = {"id": None}
    r = check_required_params(["id", "name"], params)
    assert not r['ok']
    assert "param \"id\" is empty" in r['msg']
    assert "missing param: name" in r['msg']

    params = {"id": "123"}
    r = check_required_params(["id", "name"], params)
    assert not r['ok']
    assert "missing param: name" in r['msg']

    params = {"id": "123", "name": "John"}
    r = check_required_params(["id", "name"], params)
    assert r['ok']


def test_check_string_params():
    params = {}
    r = check_string_params(["name"], params)
    assert not r['ok']
    assert "missing param: name" in r['msg']

    params = {"name": 123}
    r = check_string_params(["name"], params)
    assert not r['ok']
    assert "param \"name\" should be a string, found 123" in r['msg']

    params = {"name": "123"}
    r = check_string_params(["name"], params)
    assert r['ok']


def test_check_int_params():
    params = {}
    r = check_int_params(["name"], params)
    assert not r['ok']
    assert "missing param: name" in r['msg']

    params = {"name": "123"}
    r = check_int_params(["name"], params)
    assert not r['ok']
    assert "param \"name\" should be a int, found 123" in r['msg']

    params = {"name": 123}
    r = check_int_params(["name"], params)
    assert r['ok']
