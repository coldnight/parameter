#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This model tests ``parameter.model``."""
from __future__ import print_function, division, unicode_literals

import unittest

from parameter import Model, Argument, types, ArgumentInvalidError
from parameter import BaseAdapter, ArgumentMissError


class _TestAdapter(BaseAdapter):
    def __init__(self):
        self._info = {                             # type: dict
            "bytes": b"test",
            "string": "string",
            "string_integer": "1",
            "integer": 10,
            "string_double": "10.1",
            "double": 10.1,
            "date": "2011-11-11",
            "datetime": "2011-11-11 11:11:11",
        }

        self._multi = {
            "test": [
                "a", "b", "c"
            ]
        }

    def get_argument(self, key, default):
        return self._info.get(key, default)

    def get_arguments(self, key):
        return self._multi.get(key)


class ModelTestCase(unittest.TestCase):
    def test_string(self):
        class _TestModel(Model):
            bt = Argument("bytes", types.String)

        model = _TestModel(_TestAdapter())
        self.assertEqual(model.bt, b"test")

        class _TestModel(Model):
            bt = Argument("string", types.String)

        model = _TestModel(_TestAdapter())
        self.assertEqual(model.bt, b"string")

    def test_unicode(self):
        class _TestModel(Model):
            bt = Argument("bytes", types.Unicode)

        model = _TestModel(_TestAdapter())
        self.assertEqual(model.bt, "test")

        class _TestModel(Model):
            bt = Argument("string", types.Unicode)

        model = _TestModel(_TestAdapter())
        self.assertEqual(model.bt, "string")

    def test_max_len(self):
        class _TestModel(Model):
            bt = Argument("bytes", types.Unicode(max_len=4))

        model = _TestModel(_TestAdapter())
        self.assertEqual(model.bt, "test")

        class _TestModel(Model):
            bt = Argument("bytes", types.Unicode(max_len=3))

        with self.assertRaises(ArgumentInvalidError):
            _TestModel(_TestAdapter())

        try:
            _TestModel(_TestAdapter())
        except ArgumentInvalidError as e:
            self.assertIsInstance(e.source, types.MaxlenExceedError)

    def test_miss(self):
        class _TestModel(Model):
            null = Argument("null", types.Unicode(max_len=4))

        with self.assertRaises(ArgumentMissError):
            _TestModel(_TestAdapter())

    def test_default(self):
        class _TestModel(Model):
            null = Argument("null", types.Unicode(max_len=4), default=1)

        model = _TestModel(_TestAdapter())
        self.assertEqual(model.null, "1", "%r" % model)

    def test_multiple(self):
        class _TestModel(Model):
            multi = Argument("test", types.Unicode(max_len=4), default=1,
                             multiple=True)

        model = _TestModel(_TestAdapter())
        self.assertListEqual(model.multi, ["a", "b", "c"])
