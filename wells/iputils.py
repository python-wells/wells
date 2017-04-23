#!/usr/bin/env python
# coding=utf-8

"""
ip address utils
"""


def ip_as_int(ip_address):
    """convert dot notation to int.

    """
    parts = [int(x) for x in ip_address.split(".")]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]


def int_as_ip(ip_address):
    """convert int to dot notation

    """
    return ".".join(map(str, [ip_address >> 24,
                              (ip_address & 0b111111111111111111111111) >> 16,
                              (ip_address & 0b1111111111111111) >> 8,
                              ip_address & 0b11111111]))


def is_private_ip(ip):
    """return True if ip is a IPv4 private address or reserved address."""
    if not ip:
        return False
    # TODO use a real implementation. or rather find a good implementation.    # pylint: disable=fixme
    # http://en.wikipedia.org/wiki/IP_address#IPv4_private_addresses
    # ipaddress module is built-in in python 3.3. maybe there is a backport?
    return (ip.startswith('10.') or
            ip.startswith('127.') or
            ip.startswith('169.254.') or
            ip.startswith('172.') or
            ip.startswith('192.168.'))


def is_public_ip(ip):
    """return True if ip is a IPv4 public address."""
    if not ip:
        return False
    return not is_private_ip(ip)
