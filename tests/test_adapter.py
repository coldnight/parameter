#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module tests adapters."""
from __future__ import print_function, division, unicode_literals

import json

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from tornado import testing
from tornado import web

from parameter import Model, Argument, types
from parameter import ArgumentMissError, ArgumentInvalidError
from parameter.adapter import TornadoAdapter


class UserEntity(Model):
    username = Argument("username", types.String(max_len=100),
                        miss_message="Require username")
    password = Argument("password", types.String(max_len=64))
    name = Argument("name", types.Unicode(max_len=50))
    age = Argument("age", types.Integer, default=18)
    badges = Argument("badge", types.String, multiple=True)


class DemoHandler(web.RequestHandler):
    def get(self):
        try:
            entity = UserEntity(TornadoAdapter(self))
        except ArgumentMissError as e:
            self.write({
                "missing": True,
                "name": e.name,
            })
            return
        except ArgumentInvalidError as e:
            self.write({
                "invalid": True,
                "name": e.name,
            })

        self.write({
            "username": entity.username,
            "password": entity.password,
            "name": entity.name,
            "age": entity.age,
            "badges": entity.badges,
        })


class TornadoAdapterTestCase(testing.AsyncHTTPTestCase):
    def get_app(self):
        return web.Application([
            (r'/', DemoHandler),
        ])

    def _fetch_json(self, path, params=None):
        resp = self.fetch("/?" + urlencode(params or {}))
        self.assertEqual(resp.code, 200)
        return json.loads(resp.body)

    def test_miss(self):
        data = self._fetch_json("/")
        self.assertTrue(data["missing"])
        self.assertEqual(data["name"], "username")

    def test_ok(self):
        data = self._fetch_json("/", {
            "username": "un",
            "password": "pw",
            "age": 10,
            "name": "Gray",
        })
        self.assertDictEqual(data, {
            "username": "un",
            "password": "pw",
            "age": 10,
            "name": "Gray",
            "badges": [],
        })

    def test_multiple(self):
        data = self._fetch_json("/", [
            ("username", "uw"),
            ("password", "pw"),
            ("age", 10),
            ("name", "Gray"),
            ("badge", "1"),
            ("badge", "2"),
        ])

        self.assertDictEqual(data, {
            "username": "uw",
            "password": "pw",
            "age": 10,
            "name": "Gray",
            "badges": ["1", "2"]
        })