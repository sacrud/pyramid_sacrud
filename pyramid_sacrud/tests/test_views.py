#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Tests of viwes
"""
from collections import OrderedDict
from mock import Mock

from nose.tools import raises
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from pyramid_sacrud.security import (PYRAMID_SACRUD_CREATE,
                                     PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_LIST,
                                     PYRAMID_SACRUD_UPDATE)

from . import TransactionalTest
from ..views import sa_home
from ..views.CRUD import CRUD, Add, Delete, List
from .models import Base, Session, engine
from .models.auth import Groups, Profile, User  # noqa


class _TransactionalFixture(TransactionalTest):

    def _create_tables(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def _is_table_exist(self, table_name):
        return engine.dialect.has_table(engine.connect(), table_name)

    def _user_fixture(self, ids=(1,)):
        self._create_tables()
        for id in ids:
            user = User(name="some user %s" % id,
                        fullname="full name %s" % id,
                        password="123 %s" % id)
            user.id = id
            Session.add(user)
        Session.commit()

    def _init_pyramid_sacrud_settings(self, request):
        if not request.registry.settings:
            request.registry.settings = {}
        request.registry.settings['pyramid_sacrud.models'] = (
            ('Permissions', [User]),
            ('Users', [Groups])
        )
        return request


class InitTests(_TransactionalFixture):

    def test_bad_pk_init(self):
        request = testing.DummyRequest()
        request.matchdict["pk"] = ("foo", "bar", "baz")  # bad pk's
        request.matchdict["table"] = "user"
        request.dbsession = self.session
        with self.assertRaises(HTTPNotFound) as cm:
            CRUD(request)
        the_exception = str(cm.exception)
        self.assertEqual(the_exception, 'The resource could not be found.')

    def test_bad_table_init(self):
        request = testing.DummyRequest()
        request.matchdict["pk"] = ("foo", "bar")
        request.matchdict["table"] = "user666"
        request.dbsession = self.session
        with self.assertRaises(HTTPNotFound) as cm:
            CRUD(request)
        the_exception = str(cm.exception)
        self.assertEqual(the_exception, 'The resource could not be found.')


class HomeTests(_TransactionalFixture):

    def test_no_models_success(self):
        request = testing.DummyRequest()
        request.registry.settings = {}
        self.assertEquals(
            sa_home(request),
            {'dashboard_row_len': 3, 'tables': OrderedDict()}
        )

    def test_with_models_success(self):
        request = testing.DummyRequest()
        self._init_pyramid_sacrud_settings(request)
        responce = sa_home(request)
        self.assertEquals(responce['dashboard_row_len'], 3)
        self.assertEquals(len(responce['tables']), 2)
        tables = OrderedDict([('Permissions', [User]), ('Users', [Groups])])
        self.assertEquals(responce['tables'], tables)


class ListTests(_TransactionalFixture):

    def test_user_list_success(self):
        request = testing.DummyRequest()
        self._create_tables()
        request.dbsession = self.session
        request.matchdict['table'] = 'user'
        self._init_pyramid_sacrud_settings(request)
        responce = List(request).sa_list()
        self.assertEquals(
            responce['breadcrumbs'],
            [{'visible': True, 'name': u'Dashboard',
              'param': {'name': 'user'}, 'view': PYRAMID_SACRUD_HOME},
             {'visible': True, 'name': 'user',
              'param': {'name': 'user'}, 'view': PYRAMID_SACRUD_LIST}]
        )
        self.assertEquals(responce['table'], User)

    @raises(HTTPNotFound)
    def test_not_exist_table(self):
        self._create_tables()
        request = testing.DummyRequest()
        request.dbsession = self.session
        request.matchdict['table'] = 'not_exist_table'
        self._init_pyramid_sacrud_settings(request)
        self.assertRaises(HTTPNotFound, CRUD(request).sa_list)


class CreateTests(_TransactionalFixture):

    @raises(HTTPNotFound)
    def test_create_not_exist_form(self):
        request = testing.DummyRequest()
        request.dbsession = self.session
        request.matchdict['table'] = 'not_exist_table'
        self._init_pyramid_sacrud_settings(request)
        self.assertRaises(HTTPNotFound, Add(request).sa_add)

    def test_create_user_form(self):
        self._create_tables()
        request = testing.DummyRequest()
        request.dbsession = self.session
        request.matchdict['table'] = 'user'
        request.matched_route = Mock()
        request.matched_route.name = PYRAMID_SACRUD_CREATE
        self._init_pyramid_sacrud_settings(request)
        responce = Add(request).sa_add()
        self.assertEqual(
            responce['breadcrumbs'],
            [{'visible': True, 'name': u'Dashboard',
              'param': {'name': 'user'}, 'view': PYRAMID_SACRUD_HOME},
             {'visible': True, 'name': 'user',
              'param': {'name': 'user'}, 'view': PYRAMID_SACRUD_LIST},
             {'visible': False, 'name': 'create',
              'param': {'name': 'user'}, 'view': PYRAMID_SACRUD_LIST}]
        )
        self.assertEqual(responce['table'], User)


class UpdateTests(_TransactionalFixture):

    @raises(HTTPNotFound)
    def test_update_not_exist_form(self):
        request = testing.DummyRequest()
        request.dbsession = self.session
        request.matchdict['table'] = 'not_exist_table'
        request.matchdict['pk'] = ('id', '1')
        self._init_pyramid_sacrud_settings(request)
        self.assertRaises(HTTPNotFound, CRUD(request).sa_add)

    def test_update_user_form(self):
        self._user_fixture()
        request = testing.DummyRequest()
        request.dbsession = self.session
        request.matchdict['table'] = 'user'
        request.matchdict['pk'] = ('id', '1')
        self._init_pyramid_sacrud_settings(request)
        request.matched_route = Mock()
        request.matched_route.name = PYRAMID_SACRUD_UPDATE
        responce = Add(request).sa_add()
        self.assertEqual(
            responce['breadcrumbs'],
            [{'visible': True, 'name': u'Dashboard',
              'param': {'name': 'user'}, 'view': PYRAMID_SACRUD_HOME},
             {'visible': True, 'name': 'user',
              'param': {'name': 'user'}, 'view': PYRAMID_SACRUD_LIST},
             {'visible': False, 'name': ' id=1',
              'param': {'name': 'user'}, 'view': PYRAMID_SACRUD_LIST}]
        )
        self.assertEqual(responce['table'], User)


class DeleteTests(_TransactionalFixture):

    @raises(HTTPNotFound)
    def test_delete_not_exist_table(self):
        request = testing.DummyRequest()
        request.dbsession = self.session
        request.matchdict['table'] = 'not_exist_table'
        request.matchdict['pk'] = ('id', '1')
        self._init_pyramid_sacrud_settings(request)
        self.assertRaises(HTTPNotFound, Delete(request).sa_delete)
