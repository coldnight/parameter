#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""The base module provides the adapter base class :class:`BaseAdapter`."""
from __future__ import print_function, division, unicode_literals

import abc


class ArgumentError(Exception):
    """Argument base Exception"""
    pass


class ArgumentMissError(ArgumentError):
    pass


class ArgumentInvalidError(ArgumentError):
    pass


class BaseAdapter(object):

    @abc.abstractmethod
    def get_argument(self, name, default, *args, **kargs):
        """Returns the argument's value via ``name``.

        :param name: The name of the argument.
        :param default: The default value.

        :raises: :exception:`ArgumentMissError`
        :raises: :exception:`ArgumentInvalidError`
        """
