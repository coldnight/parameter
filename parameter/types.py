#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""The types module provides classes of argument types."""
from __future__ import print_function, division, unicode_literals

import abc
import decimal

from datetime import datetime

import six


_all_string_types = six.string_types + (six.binary_type, six.text_type)


class ConvertError(Exception):
    pass


class MismatchError(ConvertError):
    """Type mismatch."""
    pass


class MaxlenExceedError(ConvertError):
    pass


class BaseType(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def convert(self, val):
        """Convert a value to this type.

        :raises: :exception:`MismatchError`
        """
        pass


class String(BaseType):
    """String type. This is str in Python2 and bytes in Python3."""
    def __init__(self, max_len=None, encoding="utf8"):
        """Initialize

        :param max_len:
            Maximum length of the string.
        :param encoding:
            Encoding of the string.
        """

        self.max_len = max_len
        self.encoding = encoding

    def _check_max_len(self, val):
        if self.max_len is not None and len(val) > self.max_len:
            raise MaxlenExceedError(self.max_len)

    def convert(self, val):
        if isinstance(val, six.text_type):
            val = val.encode(self.encoding)
        else:
            val = six.binary_type(val)
        self._check_max_len(val)
        return val


class Unicode(String):
    """Unicode type. This is unicode in Python2 and str in Python3."""
    def convert(self, val):
        if isinstance(val, six.binary_type):
            val = val.decode("utf8")
        else:
            val = six.text_type(val)
        self._check_max_len(val)
        return val


class Integer(BaseType):
    """Integer type."""
    def convert(self, val):
        if isinstance(val, six.integer_types):
            return True

        if isinstance(val, _all_string_types):
            return val.isdigit()
        raise MismatchError(val)


class Double(BaseType):
    def convert(self, val):
        if isinstance(val, float):
            return val

        try:
            return float(val)
        except ValueError as e:
            raise MismatchError(e.message)


class Decimal(BaseType):
    def __init__(self, context=None):
        self.context = context

    def convert(self, val):
        try:
            return decimal.Decimal(val, context=self.context)
        except decimal.InvalidOperation as e:
            raise MismatchError(e.message)


class Date(BaseType):
    def __init__(self, format="%Y-%m-%d"):
        self.format = format

    def convert(self, val):
        try:
            return datetime.strptime(val, self.format).date()
        except ValueError as e:
            raise MismatchError(e.message)


class Datetime(Date):
    def __init__(self, format="%Y-%m-%d %H:%M:%S"):
        self.format = format
