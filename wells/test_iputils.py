#!/usr/bin/env python
# coding=utf-8

from .iputils import ip_as_int, int_as_ip, is_private_ip, is_public_ip


# test for ip_as_int
def test_ip_as_int():
    assert ip_as_int("0.0.0.0") == 0
    assert ip_as_int("0.0.0.1") == 1
    assert ip_as_int("1.2.3.4") == 0b00000001000000100000001100000100
    assert ip_as_int("255.0.0.0") == 0b11111111000000000000000000000000


# test for int_as_ip
def test_int_as_ip():
    assert int_as_ip(0) == "0.0.0.0"
    assert int_as_ip(1) == "0.0.0.1"
    assert int_as_ip(0b00000001000000100000001100000100) == "1.2.3.4"
    assert int_as_ip(0b11111111000000000000000000000000) == "255.0.0.0"


# test for is_private_ip
def test_is_private_ip():
    assert is_private_ip('127.0.0.1')
    assert is_private_ip('127.0.0.2')
    assert is_private_ip('10.10.10.72')
    assert is_private_ip('192.168.2.128')
    assert not is_private_ip('113.108.228.102')
    assert not is_private_ip('219.153.55.108')

    assert not is_private_ip('')
    assert not is_private_ip(None)


# test for is_public_ip
def test_is_public_ip():
    assert not is_public_ip('127.0.0.1')
    assert not is_public_ip('127.0.0.2')
    assert not is_public_ip('10.10.10.72')
    assert not is_public_ip('192.168.2.128')
    assert is_public_ip('113.108.228.102')
    assert is_public_ip('219.153.55.108')

    assert not is_public_ip('')
    assert not is_public_ip(None)
