#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""The argument module provides the :class:`Argument`."""
from __future__ import print_function, division, unicode_literals

import inspect


_DEFAULT = []       # type: list


class Argument(object):
    """Represents a parameter in HTTP request."""

    def __init__(self, name, type_, default=_DEFAULT, miss_message=None,
                 invalid_message=None):
        """Initialize

        :param name:
            The name of this argument as represented in the HTTP request.
        :param type_:
            The parameter's type, indicated using an instance which subclasses
            :class:`parameter.types.BaseType`.
        :param default:
            The default value.
        :type type_: :class:`parameter.types.BaseType`.
        :param miss_message:
            The message of :exception:`ArgumentMissError`
        :param invalid_message:
            The message of :exception:`ArgumentInvalidError`
        """
        self.name = name
        self.type_ = type_() if inspect.isclass(type_) else type_
        self.default = default
        self.miss_message = miss_message
        self.invalid_message = invalid_message

    @staticmethod
    def is_init_default(value):
        """Returns ``True`` if the ``value`` is the initial default."""
        return value is _DEFAULT
