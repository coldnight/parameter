#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Setup"""
from __future__ import print_function, division, unicode_literals

import os

from setuptools import setup

os.environ["SKIP_GENERATE_AUTHORS"] = "1"
os.environ["SKIP_WRITE_GIT_CHANGELOG"] = "1"

setup(
    setup_requires=["pbr>=1.9", "setuptools>=17.1"],
    pbr=True
)
