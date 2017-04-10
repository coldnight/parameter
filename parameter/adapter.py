#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module provides predefined adapter."""
from __future__ import print_function, division, unicode_literals

from .model import BaseAdapter


class TornadoAdapter(BaseAdapter):
    """Tornado adapter, usage::

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
