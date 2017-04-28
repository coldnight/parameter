#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module tests ``parameter.types`` module."""
from __future__ import print_function, division, unicode_literals

import decimal
import datetime

import unittest

from parameter import Model, Argument, types, ArgumentInvalidError
from parameter import BaseAdapter


class _TestAdapter(BaseAdapter):
    def __init__(self):
        self._info = {                             # type: dict
            "string": b"test",
            "unicode": "string",
            "string_int": "1",
            "integer": 10,
            "string_double": "10.1",
            "double": 10.1,
            "date": "2011-11-11",
            "datetime": "2011-11-11 11:11:11",
        }

    def get_argument(self, key, default):
        return self._info.get(key, default)

    def get_arguments(self):
        pass


class _TestModel(Model):
    string = Argument(types.String)
    unicode_ = Argument(types.Unicode, alias="unicode")
    string_int = Argument(types.Integer)
    integer = Argument(types.Integer)
    string_double = Argument(types.Double)
    double = Argument(types.Double)
    decimal = Argument(types.Decimal, alias="string_double")
    date = Argument(types.Date)
    datetime = Argument(types.Datetime)


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
            integer = Argument(types.Integer, alias="string")

        with self.assertRaises(ArgumentInvalidError):
            _Model(_TestAdapter())

    def test_double_mismatch(self):
        class _Model(Model):
            integer = Argument(types.Double, alias="string")

        with self.assertRaises(ArgumentInvalidError):
            _Model(_TestAdapter())

    def test_double(self):
        self.assertEqual(self.model.string_double, 10.1)
        self.assertEqual(self.model.double, 10.1)

    def test_decimal(self):
        self.assertEqual(self.model.decimal, decimal.Decimal("10.1"))

    def test_decimal_mismatch(self):
        class _Model(Model):
            integer = Argument(types.Decimal, alias="string")

        with self.assertRaises(ArgumentInvalidError):
            _Model(_TestAdapter())

    def test_date(self):
        self.assertEqual(self.model.date, datetime.date(2011, 11, 11))

    def test_dateime(self):
        self.assertEqual(self.model.datetime,
                         datetime.datetime(2011, 11, 11, 11, 11, 11))

    def test_datetime_mismatch(self):
        class _Model(Model):
            integer = Argument(types.Datetime, alias="string")

        with self.assertRaises(ArgumentInvalidError):
            _Model(_TestAdapter())
