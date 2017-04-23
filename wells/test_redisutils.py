#!/usr/bin/env python
# coding=utf-8

"""
test for redisutils module
"""

from __future__ import unicode_literals

from .redisutils import (ns, RedisNamespace,
                         redis_string_to_list,
                         redis_hash_to_dict)


def test_ns():
    assert ns('myapp', 'user', 'foo') == 'myapp:user:foo'
    assert ns('myapp', 'user-id-set') == 'myapp:user-id-set'


def test_namespace_class():
    ns = RedisNamespace("myapp")   # pylint: disable=redefined-outer-name
    assert ns.key('user', 'foo') == "myapp:user:foo"
    assert ns.key('user-id-set') == "myapp:user-id-set"


def test_redis_string_to_list():
    assert redis_string_to_list(b'') == []
    assert redis_string_to_list(b'a') == ['a']
    assert redis_string_to_list(b'a,b') == ['a', 'b']
    assert redis_string_to_list(b'a,b,') == ['a', 'b', '']
    assert redis_string_to_list(u'a,呵呵,哈哈'.encode('utf-8')) == ['a', '呵呵', '哈哈']


def test_redis_hash_to_dict():
    assert redis_hash_to_dict({
        b'a': b'foo',
        b'b': b'bar',
        b'c': u'嘻'.encode('utf-8'),
        b'd': None,
    }) == {
        'a': 'foo',
        'b': 'bar',
        'c': '嘻',
        'd': '',
    }
