#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module tests ``parameter.types`` module."""
from __future__ import print_function, division, unicode_literals

import decimal
import datetime

import unittest

from parameter import Model, Argument, types, ArgumentInvalidError
from parameter import BaseAdapter, ArgumentMissError


class _TestAdapter(BaseAdapter):
    def __init__(self):
        self._info = {                             # type: dict
            "string": b"test",
            "unicode": "string",
            "string_integer": "1",
            "integer": 10,
            "string_double": "10.1",
            "double": 10.1,
            "date": "2011-11-11",
            "datetime": "2011-11-11 11:11:11",
        }

    def get_argument(self, key, default):
        return self._info.get(key, default)


class _TestModel(Model):
    string = Argument("string", types.String)
    unicode_ = Argument("unicode", types.Unicode)
    string_int = Argument("string_integer", types.Integer)
    integer = Argument("integer", types.Integer)
    string_double = Argument("string_double", types.Double)
    double = Argument("double", types.Double)
    decimal = Argument("string_double", types.Decimal)
    date = Argument("date", types.Date)
    datetime = Argument("datetime", types.Datetime)


class TypesTestCase(unittest.TestCase):
    def setUp(self):
        super(TypesTestCase, self).setUp()
        self.model = _TestModel(_TestAdapter())

    def test_string(self):
        self.assertEqual(self.model.string, b"test")

    def test_unicode(self):
        self.assertEqual(self.model.unicode_, "string")

    def test_integer(self):
        self.assertEqual(self.model.string_int, 1)
        self.assertEqual(self.model.integer, 10)

    def test_integer_mismatch(self):
        class _Model(Model):
            integer = Argument("string", types.Integer)

        with self.assertRaises(ArgumentInvalidError):
            _Model(_TestAdapter())

    def test_double_mismatch(self):
        class _Model(Model):
            integer = Argument("string", types.Double)

        with self.assertRaises(ArgumentInvalidError):
            _Model(_TestAdapter())

    def test_double(self):
        self.assertEqual(self.model.string_double, 10.1)
        self.assertEqual(self.model.double, 10.1)

    def test_decimal(self):
        self.assertEqual(self.model.decimal, decimal.Decimal("10.1"))

    def test_decimal_mismatch(self):
        class _Model(Model):
            integer = Argument("string", types.Decimal)

        with self.assertRaises(ArgumentInvalidError):
            _Model(_TestAdapter())

    def test_date(self):
        self.assertEqual(self.model.date, datetime.date(2011, 11, 11))

    def test_dateime(self):
        self.assertEqual(self.model.datetime,
                         datetime.datetime(2011, 11, 11, 11, 11, 11))

    def test_datetime_mismatch(self):
        class _Model(Model):
            integer = Argument("string", types.Datetime)

        with self.assertRaises(ArgumentInvalidError):
            _Model(_TestAdapter())
