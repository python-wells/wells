wells python utilities
=======================

.. image:: https://img.shields.io/pypi/v/wells.svg
    :target: https://pypi.org/project/wells/

.. image:: https://img.shields.io/pypi/l/wells.svg
    :target: https://pypi.org/project/wells/

.. image:: https://img.shields.io/pypi/wheel/wells.svg
    :target: https://pypi.org/project/wells/

.. image:: https://img.shields.io/pypi/pyversions/wells.svg
    :target: https://pypi.org/project/wells/

.. image:: https://travis-ci.org/python-wells/wells.svg?branch=master
    :target: https://travis-ci.org/python-wells/wells/

wells is a collection of python utilities:

Most common and general utilities:

 - utils               common utilities. sequence, string and others.

Other included utilities:

 - bashscript_utils    read and write bashrc like config files (e.g. A=B)
 - config              config parser. parse simple a = b config files. Because I don't like ini sections.
 - debug               debug utilities, like @trace_time
 - fileutils           file io, like safe_read_file, safe_write_file
 - iputils             utilities to work with IP addresses
 - py3utils            python 3 portability issue helper. similar to six_.
 - redisutils          utilities when working with redis, including some converters for py3.
 - shellutils          shell related utilities

.. _six: https://pythonhosted.org/six/

Installation
------------

To install this package:

.. code-block:: bash

   $ pip install wells

Baisc Usage
------------

.. code-block:: sh

   >>> import datetime
   >>> from wells.utils import sha1sum, to_json
   >>> sha1sum("abc")
   'a9993e364706816aba3e25717850c26c9cd0d89d'
   >>> to_json({"start_date": datetime.date.today()})
   '{"start_date": "2017-04-23"}'
   >>> import wells.utils
   >>> help(wells.utils)

Documentation
-------------

External documentation is not available yet. Type help(<module_name>) to get
document in python REPL. You can also read examples in unit tests.

License
-------------

Copyright (C) 2019  Yuanle Song <sylecn@gmail.com>

This library is licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

ChangeLog
---------

* v1.0.0 2017-04-23
  - init release.
