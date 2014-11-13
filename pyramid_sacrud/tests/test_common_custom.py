#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Test for sacrud.common.custom
"""
import unittest

from pyramid_sacrud.common.custom import (get_name, Widget, WidgetRelationship,
                                          WidgetRowLambda)
from pyramid_sacrud.tests.models.auth import User


class CustomTest(unittest.TestCase):

    def test_get_name(self):
        self.assertEqual('sex', get_name(User.sex))
        self.assertEqual('id', get_name(User.id))
        self.assertEqual('user password', get_name(User.password))
        self.assertEqual('foo', get_name('foo'))

        class EmptyType: pass
        foo = EmptyType()
        foo.info = {}
        foo.name = ''
        self.assertEqual('', get_name(foo))

    def test_widget(self):
        w = Widget()
        w.name = ''
        self.assertEqual(w.info, {'verbose_name': '', 'name': ''})

        w = Widget(name='foo')
        self.assertEqual(w.info, {'verbose_name': 'foo', 'name': 'foo'})

    def test_widget_row_lambda(self):
        def func(x): return x.name + x.surname
        w = WidgetRowLambda(func, name='foo')
        self.assertEqual(w.info,
                         {'sacrud_position': 'inline',
                          'sacrud_list_content': func,
                          'verbose_name': 'foo',
                          'name': 'foo'}
                         )

    def test_widget_relationship(self):
        w = WidgetRelationship('foo', 'bar', name='baz')
        self.assertEqual(w.relation, 'foo')
        self.assertEqual(w.table, 'bar')
