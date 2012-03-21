#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Copyright (c) 2012 cloudControl GmbH

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    setup script PyDoozerLib

    usage: sudo python setup.py install
"""

from distutils.core import setup
from setuptools import find_packages
from pydoozerlib import version

DOWNLOAD_URL = 'https://github.com/downloads/cloudControl/pydoozerlib/' \
               'pydoozerlib-{0}.tar.gz'.format(version.__version__)

setup(
    name="PyDoozerLib",
    version=version.__version__,
    description='cloudControl\'s Doozer client library for Python.',
    author='cloudControl Team',
    author_email='info@cloudcontrol.de',
    url='https://github.com/cloudControl/pydoozerlib',
    install_requires=['protobuf'],
    packages=find_packages(),
    download_url=DOWNLOAD_URL,
    license='MIT'
)
