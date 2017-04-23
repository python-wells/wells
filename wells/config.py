#!/usr/bin/env python
# coding=utf-8

"""
configuration manager
"""

import os.path
import logging


from . import fileutils


logger = logging.getLogger(__name__)


class BadConfig(Exception):
    pass


class ConfigurationManger(object):

    def read_file_content(self, content):
        """parse a file and store/update key/value pairs in self.data.

        """
        for line in content.split("\n"):
            line = line.strip()
            if not line:
                # ignore empty lines
                continue
            if line.startswith("#") or line.startswith(";"):
                # ignore comment lines
                continue
            try:
                key, value = line.split("=", 1)
            except ValueError:
                logger.error(u"bad line in config file: %s", line)
                raise BadConfig(u"bad line in config file: %s" % (line,))
            key = key.strip()
            value = value.strip()
            if key not in self.all_possible_keys:
                logger.warning(u"ignoring unsupported key: %s", key)
            self.data[key] = value

    def __init__(self,
                 defaults=None,
                 configfiles=None,
                 required_keys=None,
                 optional_keys=None):
        """create a CONF object.

        Args:
            defaults: a dict contains key value pairs
            configfiles: a list of file names

        Return:
            True if config file parse is successful, False otherwise.

        """
        self.required_keys = required_keys or []
        self.optional_keys = optional_keys or []
        self.all_possible_keys = self.required_keys + self.optional_keys
        for k in defaults.keys():
            if k not in self.all_possible_keys:
                logger.warning(u"ignoring unsupported key: %s", k)
        self.data = defaults or {}
        self.configfiles = configfiles or []
        for fn in configfiles:
            r = fileutils.safe_read_file(fn)
            if r['ok']:
                self.read_file_content(r['content'])
            else:
                if os.path.exists(fn):
                    logger.error(u"%s", r['msg'])
                    raise BadConfig("reading config file %s has failed: %s"
                                    % (fn, r['msg']))
        missing_keys = []
        for key in self.required_keys:
            if key not in self.data:
                missing_keys.append(key)
        if missing_keys:
            msg = u"missing required key: %s" % (", ".join(missing_keys),)
            logger.error(u"%s", msg)
            raise BadConfig(msg)

    def getstr(self, key, default=None):
        return self.data.get(key, default)

    def getbool(self, key, default=False):
        try:
            return self.data[key] in ["True", "true", "Yes", "yes", "1"]
        except KeyError:
            return default

    def getfloat(self, key, default=0.0):
        try:
            return float(self.data[key])
        except KeyError:
            return default
        except ValueError:
            logger.error(u"CONF.getfloat failed for value: %s", self.data[key])
            raise

    def getint(self, key, default=0):
        try:
            return int(self.data[key])
        except KeyError:
            return default
        except ValueError:
            logger.error(u"CONF.getint failed for value: %s", self.data[key])
            raise

    def __iter__(self):
        try:
            return self.data.iteritems()
        except AttributeError:
            return self.data.items()
