wells python utilities
=======================

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

Documentation
-------------

No external documentation available. type help(<module_name>) to get
auto-generated document. You can also read examples in unit tests.

ChangeLog
---------

* v1.0.0 2017-04-23
  - init release.
