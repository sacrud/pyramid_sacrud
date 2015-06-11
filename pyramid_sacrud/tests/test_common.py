#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Test common module of pyramoid_sacrud
"""
import unittest

import colander
from pyramid import testing
from pyramid_sacrud.breadcrumbs import breadcrumbs, get_crumb
from pyramid_sacrud.common import (get_settings_param, get_table,
                                   get_table_verbose_name, import_from_string,
                                   preprocessing_value)
from pyramid_sacrud.security import (
    PYRAMID_SACRUD_CREATE, PYRAMID_SACRUD_HOME,
    PYRAMID_SACRUD_LIST, PYRAMID_SACRUD_UPDATE
)

from .models.auth import User
from .test_views import _TransactionalFixture


class SilentNoneTest(unittest.TestCase):
    # TODO:
    # >>> _silent_none(0)
    # 0
    # >>> _silent_none('foo')
    # 'foo'
    # >>> _silent_none(None)
    # ''
    # >>> _silent_none('None')
    # ''
    # >>> _silent_none(False)
    # ''
    # >>> class Foo(object):
    # ...   def __bool__(self):
    # ...     return False
    # >>> _silent_none(Foo)
    # <class 'pyramid_sacrud.common.Foo'>
    # >>> _silent_none(u'ПревеД!')
    # u'\\xd0\\x9f\\xd1\\x80\\xd0\\xb5\\xd0\\xb2\\xd0\\xb5\\xd0\\x94!'
    pass


class BreadCrumbsTest(unittest.TestCase):

    def test_get_crumb(self):
        crumb = get_crumb(
            'Dashboard', True, PYRAMID_SACRUD_HOME, {'name': 'foo'})
        self.assertEqual(crumb, {'visible': True, 'name': 'Dashboard',
                                 'param': {'name': 'foo'},
                                 'view': PYRAMID_SACRUD_HOME})

    def test_breadcrumbs(self):
        bc = breadcrumbs('foo', 'ffoo', PYRAMID_SACRUD_LIST)
        self.assertEqual(
            bc,
            [{'visible': True, 'name': u'Dashboard',
              'param': {'name': 'foo'},
              'view': PYRAMID_SACRUD_HOME},
             {'visible': True, 'name': 'ffoo',
              'param': {'name': 'foo'}, 'view': PYRAMID_SACRUD_LIST}])

        bc = breadcrumbs('foo', 'barr', PYRAMID_SACRUD_CREATE)
        self.assertEqual(
            bc,
            [{'visible': True, 'name': 'Dashboard',
              'param': {'name': 'foo'}, 'view': PYRAMID_SACRUD_HOME},
             {'visible': True, 'name': 'barr',
              'param': {'name': 'foo'}, 'view': PYRAMID_SACRUD_LIST},
             {'visible': False, 'name': 'create',
              'param': {'name': 'foo'}, 'view': PYRAMID_SACRUD_LIST}])

        bc = breadcrumbs('foo', 'bazz', PYRAMID_SACRUD_UPDATE)
        self.assertEqual(
            bc,
            [{'visible': True, 'name': 'Dashboard',
              'param': {'name': 'foo'}, 'view': PYRAMID_SACRUD_HOME},
             {'visible': True, 'name': 'bazz',
              'param': {'name': 'foo'}, 'view': PYRAMID_SACRUD_LIST},
             {'visible': False, 'name': None,
              'param': {'name': 'foo'}, 'view': PYRAMID_SACRUD_LIST}])


class CommonTest(_TransactionalFixture):

    def test_preprocessing_value(self):
        self.assertEqual(None,
                         preprocessing_value(colander.null))
        value = {'foo': 'bar'}
        self.assertEqual(value,
                         preprocessing_value(value))

    def test_get_obj_from_settings(self):
        request = testing.DummyRequest()
        config = testing.setUp(request=request)
        config.registry.settings['foo.User'] =\
            'pyramid_sacrud.tests.models.auth:User'
        obj = get_settings_param(request, 'foo.User')
        self.assertEqual(obj, User)

        config.registry.settings['foo.User'] = User
        obj = get_settings_param(request, 'foo.User')
        self.assertEqual(obj, User)

        config.registry.settings['foo.User'] = 'bad string'
        obj = get_settings_param(request, 'foo.User')
        self.assertEqual(obj, None)

    def test_import_from_string(self):
        self.assertEqual(
            User,
            import_from_string('pyramid_sacrud.tests.models.auth:User'))
        self.assertEqual(
            User,
            import_from_string(User))

    def test_get_table(self):
        request = testing.DummyRequest()
        self._init_pyramid_sacrud_settings(request)

        user = get_table('UsEr', request)
        self.assertEqual(user, User)

        foo = get_table('foo', request)
        self.assertEqual(foo, None)

        request.registry.settings['pyramid_sacrud.models'] = (
            ('Permissions', [User])
        )
        user = get_table('useR', request)
        self.assertEqual(user, User)
        user = get_table('User', request)
        self.assertEqual(user, User)

    def test_get_table_verbose_name(self):
        class Foo(object):
            name = 'foo'

        class Bar(object):
            __tablename__ = 'bar'

        class Baz(object):
            verbose_name = 'baz'
        self.assertEqual('foo', get_table_verbose_name(Foo))
        self.assertEqual('bar', get_table_verbose_name(Bar))
        self.assertEqual('baz', get_table_verbose_name(Baz))
