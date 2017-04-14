#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Exceptions of this package."""
from __future__ import print_function, division, unicode_literals


class ParameterException(Exception):
    """Base exception of this package."""
    pass


class ConvertError(ParameterException):
    pass


class MismatchError(ConvertError):
    """Type mismatch."""
    pass


class MaxlenExceedError(ConvertError):
    pass


class ArgumentError(ParameterException):
    """Argument base Exception"""
    def __init__(self, message, name):
        """Initialize

        :param message: Invalid message.
        :param name: Argument name.
        """
        super(ArgumentError, self).__init__(message)
        self.name = name


class ArgumentMissError(ArgumentError):
    pass


class ArgumentInvalidError(ArgumentError):
    def __init__(self, message, name, source):
        """Initialize

        :param message: Invalid message.
        :param name: Argument name.
        :param source: Source exception.
        """
        super(ArgumentInvalidError, self).__init__(message, name)
        self.source = source
