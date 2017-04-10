#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Model and Argument."""
from __future__ import print_function, division, unicode_literals

import abc
import inspect

import six

from .types import ConvertError


class ArgumentError(Exception):
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


@six.add_metaclass(abc.ABCMeta)
class BaseAdapter(object):

    @abc.abstractmethod
    def get_argument(self, name, default, *args, **kwargs):
        """Returns the argument's value via ``name``.

        :param name: The name of the argument.
        :param default: The default value.
        :raises: :exception:`ArgumentMissError`
        :raises: :exception:`ArgumentInvalidError`
        """

    @abc.abstractmethod
    def get_arguments(self, name, *args, **kwargs):
        """Returns the argument's values via ``name``.

        :param name: The name of the argument.
        :raises: :exception:`ArgumentMissError`
        :raises: :exception:`ArgumentInvalidError`
        """


class Argument(object):
    """Represents a parameter in HTTP request."""

    _DEFAULT = []       # type: list

    def __init__(self, name, type_, default=_DEFAULT, multiple=False,
                 miss_message=None, invalid_message=None):
        """Initialize

        :param name:
            The name of this argument as represented in the HTTP request.
        :param type_:
            The parameter's type, indicated using an instance which subclasses
            :class:`parameter.types.BaseType`.
        :type type_: :class:`parameter.types.BaseType`.
        :param default: The default value.
        :param multiple: This argument have multiple values.
        :param miss_message:
            The message of :exception:`ArgumentMissError`
        :param invalid_message:
            The message of :exception:`ArgumentInvalidError`
        """
        self.name = name
        self.type_ = type_() if inspect.isclass(type_) else type_
        self.default = default
        self.multiple = multiple
        self.miss_message = miss_message
        self.invalid_message = invalid_message

    @classmethod
    def is_init_default(cls, value):
        """Returns ``True`` if the ``value`` is the initial default."""
        return value is cls._DEFAULT

    def convert(self, value):
        """Check and convert the value to the specified type.

        :raises: :exception:`ArgumentMissError`
        :raises: :exception:`ArgumentInvalidError`
        """
        if self.is_init_default(value):
            raise ArgumentMissError(self.miss_message, self.name)

        try:
            return self.type_.convert(value)
        except ConvertError as e:
            raise ArgumentInvalidError(self.invalid_message, self.name, e)


class ModelMeta(type):
    def __new__(cls, name, base, __dict__):
        arguments = [(attr, val) for attr, val in __dict__.items()
                     if isinstance(val, Argument)]
        __dict__["_meta_arguments"] = arguments

        for key, _ in arguments:
            __dict__.pop(key)

        return type.__new__(cls, name, base, __dict__)


@six.add_metaclass(ModelMeta)
class Model(object):
    _meta_arguments = None       # type: list

    def __init__(self, adapter):
        """Initialize

        :param adapter:
            The adapter to get argument,
            indicate using an instance which subclasses
            :class:`BaseAdapter`
        :type adapter: :class:`BaseAdapter`
        """
        self.adapter = adapter
        self._arguments = {}

        for attr, arg in self._meta_arguments:
            if arg.multiple:
                val = self.adapter.get_arguments(arg.name)
                val = [arg.convert(v) for v in val]
            else:
                val = self.adapter.get_argument(arg.name, arg.default)
                val = arg.convert(val)

            self._arguments[attr] = val

    def __getattr__(self, key):
        return self._arguments[key]

    def __repr__(self):
        args = " ".join("<%s: %s>" % (attr, arg.type_.__class__.__name__)
                        for attr, arg in self._meta_arguments)
        return "<%s [%s]>" % (self.__class__.__name__, args)
