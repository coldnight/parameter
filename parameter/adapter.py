#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module provides predefined adapter."""
from __future__ import print_function, division, unicode_literals

import json

import six

from .model import BaseAdapter
from .exception import ArgumentInvalidError


class TornadoAdapter(BaseAdapter):
    """Tornado adapter.

    Usage::

        from tornado import web

        from parameter import Model, Argument, types
        from parameter.adapter import TornadoAdapter


        class UserEntity(Model):
            username = Argument("username", types.String, max_len=100)
            password = Argument("password", types.String, max_len=64)
            name = Argument("name", types.Unicode, max_len=50)
            arg = Argument("age", types.Integer, default=18)


        class DemoHandler(web.RequestHandler):
            def get(self):
                entity = UserEntity(TornadoAdapter(self))

                self.write({
                    "name": entity.name,
                    "age": entity.age,
                })
    """

    def __init__(self, handler):
        """Initialize

        :param handler: Instance of Tornao RequestHandler.
        :type handler: :class:`tornado.web.RequestHandler`
        """
        self.handler = handler

    def get_argument(self, name, default, *args, **kwargs):
        return self.handler.get_argument(name, default=default, *args,
                                         **kwargs)

    def get_arguments(self, name, *args, **kwargs):
        return self.handler.get_arguments(name, *args, **kwargs)


class JSONAdapter(BaseAdapter):
    """JSON adapter to get arguments from a JSON object.

    Usage::

        from parameter import Model, Argument, types
        from parameter.adapter import JSONAdapter

        data = {"a": 1, "b": 2}

        class DataEntity(Model):
            a = Argument("a", types.Integer)
            b = Argument("b", types.Integer)

        adapter = JSONAdapter(data)
        entity = DataEntity(adapter)

        print(entity.a)         # 1
        print(entity.b)         # 2


    Nested::

        from parameter import Model, Argument, types
        from parameter.adapter import JSONAdapter

        data = {"a": 1, "b": 2, "person": {"age": 18, "name": "Gray"}}

        class PersonEntity(Model):
            are = Argument("age", types.Integer)
            name = Argument("name", types.Unicode)

        class DataEntity(Model):
            a = Argument("a", types.Integer)
            b = Argument("b", types.Integer)
            person = Argument("person", types.Nested(PersonEntity))

        adapter = JSONAdapter(data)
        entity = DataEntity(adapter)

        print(entity.a)         # 1
        print(entity.b)         # 2
        print(entity.person.age)    # 18
        print(entity.person.name)   # Gray
    """

    def __init__(self, data):
        """Initialize

        :param data:
            JSON Data, it can be an instance of str or dict,
            if it is an instance of str it must be an json string.
        """

        if isinstance(data, six.binary_type):
            data = data.decode("utf8")

        if isinstance(data, six.text_type):
            data = json.loads(data)

        if not isinstance(data, dict):
            raise TypeError("``data`` must be a json string or dict")

        self.data = data

    def get_argument(self, name, default):
        return self.data.get(name, default)

    def get_arguments(self, name):
        ret = self.data.get(name)

        if not isinstance(ret, (list, tuple)):
            raise ArgumentInvalidError(
                "``%s`` except a sequence, but got %s." % (
                    name, type(ret)), name, TypeError())

        return ret

    @staticmethod
    def spawn(data):
        return JSONAdapter(data)
