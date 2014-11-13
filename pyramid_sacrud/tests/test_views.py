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
from nose.tools import raises
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from . import TransactionalTest
from ..views import sa_home
from ..views.CRUD import CRUD, Add, List, Delete
from .models import engine, Session, Base
from .models.auth import Groups, User


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
        request.registry.settings['pyramid_sacrud.models'] =\
            {
                'Permissions': {
                    'tables': (
                        User,
                    ),
                    'position': 1,
                },
                'Users': {
                    'tables': (
                        Groups,
                    ),
                    'position': 4,
                }
            }
        return request


class InitTests(_TransactionalFixture):

    def test_bad_pk_init(self):
        request = testing.DummyRequest()
        request.matchdict["pk"] = ("foo", "bar", "baz")  # bad pk's
        request.matchdict["table"] = "user"
        with self.assertRaises(HTTPNotFound) as cm:
            CRUD(request)
        the_exception = str(cm.exception)
        self.assertEqual(the_exception, 'The resource could not be found.')

    def test_bad_table_init(self):
        request = testing.DummyRequest()
        request.matchdict["pk"] = ("foo", "bar")
        request.matchdict["table"] = "user666"
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
            {'widgets': [], 'dashboard_columns': 3}
        )

    def test_with_models_success(self):
        request = testing.DummyRequest()
        self._init_pyramid_sacrud_settings(request)
        responce = sa_home(request)
        self.assertEquals(responce['dashboard_columns'], 3)
        self.assertEquals(len(responce['widgets']), 4)
        self.assertEquals(responce['widgets'][0].tables, (User,))
        self.assertEquals(responce['widgets'][0].position, 1)
        self.assertEquals(responce['widgets'][1].tables, [])
        self.assertEquals(responce['widgets'][2].tables, [])
        self.assertEquals(responce['widgets'][3].tables, (Groups,))
        self.assertEquals(responce['widgets'][3].position, 4)


class ListTests(_TransactionalFixture):

    def test_user_list_success(self):
        request = testing.DummyRequest()
        self._create_tables()
        request.dbsession = self.session
        request.matchdict['table'] = 'user'
        self._init_pyramid_sacrud_settings(request)
        responce = List(request).sa_list()
        self.assertEquals(responce['breadcrumbs'],
                          [{'visible': True, 'name': u'Dashboard',
                            'param': {'name': 'user'}, 'view': 'sa_home'},
                           {'visible': True, 'name': 'user',
                            'param': {'name': 'user'}, 'view': 'sa_list'}]
                          )
        self.assertEquals(responce['sa_crud']['table'], User)

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
        request = testing.DummyRequest()
        request.dbsession = self.session
        request.matchdict['table'] = 'user'
        self._init_pyramid_sacrud_settings(request)
        responce = Add(request).sa_add()
        self.assertEqual(responce['breadcrumbs'],
                         [{'visible': True, 'name': u'Dashboard', 'param': {'name': 'user'},
                           'view': 'sa_home'},
                          {'visible': True, 'name': 'user', 'param': {'name': 'user'},
                           'view': 'sa_list'},
                          {'visible': False, 'name': 'create', 'param': {'name': 'user'},
                           'view': 'sa_list'}]
                         )
        self.assertEqual(responce['sa_crud']['table'], User)


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
        responce = Add(request).sa_add()
        self.assertEqual(responce['breadcrumbs'],
                         [{'visible': True, 'name': u'Dashboard', 'param': {'name': 'user'},
                           'view': 'sa_home'},
                          {'visible': True, 'name': 'user', 'param': {'name': 'user'},
                           'view': 'sa_list'},
                          {'visible': False, 'name': ' id=1', 'param': {'name': 'user'},
                           'view': 'sa_list'}]
                         )
        self.assertEqual(responce['sa_crud']['table'], User)


class DeleteTests(_TransactionalFixture):

    @raises(HTTPNotFound)
    def test_delete_not_exist_table(self):
        request = testing.DummyRequest()
        request.dbsession = self.session
        request.matchdict['table'] = 'not_exist_table'
        request.matchdict['pk'] = ('id', '1')
        self._init_pyramid_sacrud_settings(request)
        self.assertRaises(HTTPNotFound, Delete(request).sa_delete)
