#!/usr/bin/env python
# coding=utf-8

"""
python distribute file
"""

from setuptools import setup, find_packages

# make sure I can import wells without installing any dependency, otherwise,
# this will fail.
from wells import __version__


setup(
    name="wells",
    version=__version__,
    packages=find_packages(),
    install_requires=[],
    author="Yuanle Song",
    author_email="sylecn@gmail.com",
    maintainer="Yuanle Song",
    maintainer_email="sylecn@gmail.com",
    description="wells python utilities",
    long_description=open('README.rst').read(),
    license="LGPLv3+",
    url="https://pypi.python.org/pypi/wells",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
