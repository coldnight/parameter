#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" """
from __future__ import print_function, division, unicode_literals

import six

from .argument import Argument
from .adapter.base import ArgumentMissError, ArgumentInvalidError
from .types import ConvertError


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
            :class:`~parameter.adapter.base.BaseAdapter`
        :type adapter:
            :class:`parameter.adapter.base.BaseAdapter`
        """
        self.adapter = adapter
        self._arguments = {}

        for attr, arg in self._meta_arguments:
            val = self.adapter.get_argument(arg.name, arg.default)

            if arg.is_init_default(val):
                raise ArgumentMissError(arg.miss_message)

            try:
                self._arguments[attr] = arg.type_.convert(val)
            except ConvertError:
                raise ArgumentInvalidError(arg.invalid_message)

    def __getattr__(self, key):
        return self._arguments[key]
