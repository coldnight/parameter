#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module tests adapters."""
from __future__ import print_function, division, unicode_literals

import json
import unittest

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from tornado import testing
from tornado import web

from parameter import Model, Argument, types
from parameter import ArgumentMissError, ArgumentInvalidError
from parameter.adapter import TornadoAdapter, JSONAdapter


class UserEntity(Model):
    username = Argument(types.String(max_len=100))
    password = Argument(types.String(max_len=64))
    name = Argument(types.Unicode(max_len=50))
    age = Argument(types.Integer, default=18)
    badges = Argument(types.Unicode, multiple=True, alias="badge")


class SingleArgEntity(Model):
    username = Argument(types.String(max_len=100),
                        miss_message="Require username")


class DemoHandler(web.RequestHandler):
    def get(self):
        try:
            if self.request.path == "/":
                entity = UserEntity(TornadoAdapter(self))
            else:
                entity = SingleArgEntity(TornadoAdapter(self))
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
            "username": entity.username.decode("utf8"),
            "password": entity.password.decode('utf8'),
            "name": entity.name,
            "age": entity.age,
            "badges": entity.badges,
        })


class TornadoAdapterTestCase(testing.AsyncHTTPTestCase):
    def get_app(self):
        return web.Application([
            (r'/', DemoHandler),
            (r'/1', DemoHandler),
        ])

    def _fetch_json(self, path, params=None):
        resp = self.fetch(path + "?" + urlencode(params or {}))
        self.assertEqual(resp.code, 200)
        return json.loads(resp.body.decode('utf8'))

    def test_miss(self):
        data = self._fetch_json("/1")
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


class DemoEntity(Model):
    a = Argument(types.Integer)
    b = Argument(types.Integer)


class JSONAdapterTestCase(unittest.TestCase):
    def test_binary_string(self):
        adapter = JSONAdapter(b'{"a": 1, "b": 2}')

        entity = DemoEntity(adapter)

        self.assertEqual(entity.a, 1)
        self.assertEqual(entity.b, 2)

    def test_text_string(self):
        adapter = JSONAdapter('{"a": 1, "b": 2}')

        entity = DemoEntity(adapter)

        self.assertEqual(entity.a, 1)
        self.assertEqual(entity.b, 2)

    def test_dict(self):
        adapter = JSONAdapter({"a": 1, "b": 2})

        entity = DemoEntity(adapter)

        self.assertEqual(entity.a, 1)
        self.assertEqual(entity.b, 2)

    def test_not_dict(self):
        with self.assertRaises(TypeError):
            JSONAdapter([])

    def test_nested(self):
        class NestedEntity(Model):
            demo = Argument(types.Nested(DemoEntity))
            c = Argument(types.Integer)

        adapter = JSONAdapter({"demo": {"a": 1, "b": 2}, "c": 3})
        entity = NestedEntity(adapter)

        self.assertEqual(entity.c, 3)
        self.assertEqual(entity.demo.a, 1)
        self.assertEqual(entity.demo.b, 2)

    def test_multiple_nested(self):
        class NestedEntity(Model):
            demos = Argument(types.Nested(DemoEntity), multiple=True,
                             alias="demo")
            c = Argument(types.Integer)

        adapter = JSONAdapter({"demo": [
            {"a": 1, "b": 2},
            {"a": 4, "b": 5}
        ], "c": 3})
        entity = NestedEntity(adapter)

        self.assertEqual(entity.c, 3)
        self.assertEqual(entity.demos[0].a, 1)
        self.assertEqual(entity.demos[0].b, 2)

        self.assertEqual(entity.demos[1].a, 4)
        self.assertEqual(entity.demos[1].b, 5)

    def test_multiple_nested_type_error(self):
        class NestedEntity(Model):
            demos = Argument(types.Nested(DemoEntity), multiple=True)
            c = Argument(types.Integer)

        adapter = JSONAdapter({"demo": {"a": 1, "b": 2}, "c": 3})

        with self.assertRaises(ArgumentInvalidError):
            NestedEntity(adapter)

    def test_nested_model_cls_type_error(self):
        with self.assertRaises(TypeError):
            class NestedEntity(Model):
                demos = Argument(types.Nested([]), alias="demo", multiple=True)
                c = Argument(types.Integer)

    def test_nested_model_cls_value_error(self):
        class T(object):
            pass

        with self.assertRaises(ValueError):
            class NestedEntity(Model):
                demos = Argument(types.Nested(T), alias="demo", multiple=True)
                c = Argument(types.Integer)
