#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import datetime

from .utils import (uniq, group, first, len_gen, gen_prefixes,
                    is_valid_uuid, sha1sum, md5sum, hmac_sha256_hex,
                    seconds, drop_prefix, string_to_list,
                    ensure_str, ensure_byte, to_json)
from .utils import flatten
from .utils import now


def test_now():
    assert len(now()) == len('YYYY-MM-DD HH:MM:SS')


# test for flatten
def test_flatten():
    assert list(flatten([[1, 2, 3], [4, 5]])) == [1, 2, 3, 4, 5]
    assert list(flatten([[1, 2, 3], []])) == [1, 2, 3]
    assert list(flatten([[1, 2, 3], [], [6]])) == [1, 2, 3, 6]


# test for drop_prefix
def test_drop_prefix():
    assert drop_prefix("", "") == ""
    assert drop_prefix("abc", "") == ""
    assert drop_prefix("", "abc") == "abc"
    assert drop_prefix("def", "abc") == "abc"
    assert drop_prefix("a", "abc") == "bc"
    assert drop_prefix("ab", "abc") == "c"
    assert drop_prefix("abc", "abc") == ""
    assert drop_prefix("abcd", "abc") == "abc"


# test for uniq
def test_uniq():
    assert list(uniq((1, 2, 1, 3, 1, 5))) == [1, 2, 3, 5]
    assert list(uniq((1, 5, 1, 3, 1, 2))) == [1, 5, 3, 2]
    assert list(uniq((1, 1, 1, 3, 6, 3))) == [1, 3, 6]
    assert list(uniq(())) == []


# test for group
def test_group():
    def _group(*args, **kwargs):
        return list(group(*args, **kwargs))
    assert _group(1, [1, 2, 3, 4, 5]) == [[1], [2], [3], [4], [5]]
    assert _group(2, [1, 2, 3, 4, 5]) == [[1, 2], [3, 4], [5]]
    assert _group(6, [1, 2, 3, 4, 5]) == [[1, 2, 3, 4, 5]]
    assert _group(1, []) == []

    assert _group(2, "12345", value_constructor="".join) == ["12", "34", "5"]


# test for first
def test_first():
    assert first(lambda x: x > 0, [-1, 1, 2, 3]) == 1
    assert first(lambda x: x > 0, [1, 2, 3]) == 1
    assert first(lambda x: x > 0, [-1, -2, -3]) is None
    assert first(lambda x: x > 0, []) is None


# test for len_gen
def test_len_gen():
    assert len_gen((x for x in [1, 2, 3])) == 3
    assert len_gen((x for x in [])) == 0
    assert len_gen((x for x in [1, 2, 3, 4] if x == 3)) == 1


# test for len_gen
def test_len_gen_twice():
    g = (x for x in [1, 2, 3])
    assert len_gen(g) == 3
    assert len_gen(g) == 0


# test for gen_prefixes
def test_gen_prefixes():
    assert list(gen_prefixes("abc")) == ["a", "ab", "abc"]
    assert list(gen_prefixes("")) == []
    assert list(gen_prefixes("a")) == ["a"]
    assert list(gen_prefixes("abc", 2)) == ["ab", "abc"]
    assert list(gen_prefixes("abc", 3)) == ["abc"]
    assert list(gen_prefixes("abc", 4)) == []


# test for is_valid_uuid
def test_is_valid_uuid():
    r = "dd553263-8b0c-40e4-9370-ab10c7b0172b"
    assert is_valid_uuid("dd553263-8b0c-40e4-9370-ab10c7b0172b") == r
    assert is_valid_uuid("DD553263-8B0C-40E4-9370-AB10C7B0172B") == r
    assert is_valid_uuid("{DD553263-8B0C-40E4-9370-AB10C7B0172B}") == r


# test for sha1sum
def test_sha1sum():
    assert sha1sum("") == "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    assert sha1sum("a") == "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8"
    assert sha1sum(b"a") == "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8"
    assert sha1sum("\n") == "adc83b19e793491b1c6ea0fd8b46cd9f32e592fc"


# test for md5sum
def test_md5sum():
    assert md5sum("") == "d41d8cd98f00b204e9800998ecf8427e"
    assert md5sum("a") == "0cc175b9c0f1b6a831c399e269772661"
    assert md5sum(b"a") == "0cc175b9c0f1b6a831c399e269772661"


def test_hmac_sha256_hex():
    assert hmac_sha256_hex(b'ZoBKuQXji6bs1VSmWOwgfa+Z', b'some message') == (
        '7813296e166a69f9ed3d5a263a8d59f66efabcb1a319449cbfe9a5452773e93f')
    assert hmac_sha256_hex('ZoBKuQXji6bs1VSmWOwgfa+Z', b'some message') == (
        '7813296e166a69f9ed3d5a263a8d59f66efabcb1a319449cbfe9a5452773e93f')


# test for seconds
def test_seconds():
    assert seconds("1") == 1
    assert seconds("2") == 2
    assert seconds("10m") == 10 * 60
    assert seconds("10min") == 10 * 60
    assert seconds("10h") == 10 * 3600
    assert seconds("10d") == 10 * 24 * 3600

    assert seconds(1234) == 1234


# test for seconds
def test_seconds_bad():
    try:
        seconds([])
        assert False
    except ValueError as _:
        pass
    try:
        seconds("98y")
        assert False
    except ValueError as _:
        pass


def test_string_to_list():
    assert string_to_list("") == []
    assert string_to_list("abc") == ["abc"]
    assert string_to_list("abc,def") == ["abc", "def"]
    assert string_to_list("abc, def") == ["abc", " def"]
    assert string_to_list("abc|def") == ["abc|def"]
    assert string_to_list("abc |def") == ["abc |def"]
    assert string_to_list("abc|def", sep="|") == ["abc", "def"]
    assert string_to_list("abc |def", sep="|") == ["abc ", "def"]


def test_ensure_str():
    assert ensure_str(b'abc123') == u'abc123'
    assert ensure_str(u'123') == u'123'
    assert ensure_str(u'中文') == u'中文'


def test_ensure_byte():
    assert ensure_byte(b'abc123') == b'abc123'
    assert ensure_byte(u'123') == u'123'.encode('utf-8')
    assert ensure_byte(u'中文') == u'中文'.encode('utf-8')


def test_to_json():
    assert to_json([1, 2, 3, "4"]) == '[1, 2, 3, "4"]'
    assert to_json({"a": 1, "b": 2}) in ('{"a": 1, "b": 2}',
                                         '{"b": 2, "a": 1}')
    assert to_json(datetime.date(2016, 1, 2)) == '"2016-01-02"'
    assert to_json({"name": "foo",
                    "birth": datetime.date(2016, 1, 2)}) in (
                        '{"name": "foo", "birth": "2016-01-02"}',
                        '{"birth": "2016-01-02", "name": "foo"}')


def test_to_json_kwargs():
    assert to_json(["abc", "def"], indent=4) in ("""\
[
    "abc", \n\
    "def"
]""", """\
[
    "abc",
    "def"
]""")                           # py2 has the extra space after comma
