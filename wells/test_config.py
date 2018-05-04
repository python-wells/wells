#!/usr/bin/env python
# coding=utf-8

"""
unit test for config.py
"""

from __future__ import print_function, unicode_literals

import os

from .config import env_var_key, ConfigurationManger


# test for env_var_key
def test_env_var_key():
    assert env_var_key("db.host") == "DB_HOST"
    assert env_var_key("host") == "HOST"
    assert env_var_key("port") == "PORT"
    assert env_var_key("api.admin-token") == "API_ADMIN_TOKEN"


def test_env_var_override():
    cm = ConfigurationManger(defaults={"db.host": "127.0.0.1"})
    assert cm.getstr("db.host") == "127.0.0.1"

    os.environ["DB_HOST"] = "0.0.0.0"
    os.environ["DB_PORT"] = "5433"
    cm2 = ConfigurationManger(defaults={"db.host": "127.0.0.1"})
    assert cm2.getstr("db.host") == "0.0.0.0"
    assert cm2.getstr("db.port") is None

    # read env is done at object constructor time.
    assert cm.getstr("db.host") == "127.0.0.1"
