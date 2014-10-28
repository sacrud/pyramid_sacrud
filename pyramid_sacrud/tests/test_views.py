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
from ..views.CRUD import CRUD
from .models import engine, Session
from .models.auth import Groups, Profile, User


class _TransactionalFixture(TransactionalTest):

    def _create_tables(self):
        User.__table__.create(engine, checkfirst=True)
        Profile.__table__.create(engine, checkfirst=True)

    def _user_fixture(self):
        self._create_tables()
        user = User(name="some user", fullname="full name", password="123")
        Session.add(user)
        return user

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
        self._user_fixture()
        request.dbsession = self.session
        request.matchdict['table'] = 'user'
        self._init_pyramid_sacrud_settings(request)
        responce = CRUD(request).sa_list()
        self.assertEquals(responce['breadcrumbs'],
                          [{'visible': True, 'name': u'Dashboard',
                            'param': {'name': 'user'}, 'view': 'sa_home'},
                           {'visible': True, 'name': 'user',
                            'param': {'name': 'user'}, 'view': 'sa_list'}]
                          )
        self.assertEquals(responce['sa_crud']['table'], User)

    @raises(HTTPNotFound)
    def test_not_exist_table(self):
        self._user_fixture()

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
        self.assertRaises(HTTPNotFound, CRUD(request).sa_add)

    def test_create_user_form(self):
        request = testing.DummyRequest()
        request.dbsession = self.session
        request.matchdict['table'] = 'user'
        self._init_pyramid_sacrud_settings(request)
        responce = CRUD(request).sa_add()
        self.assertEqual(responce['breadcrumbs'],
                         [{'visible': True, 'name': u'Dashboard', 'param': {'name': 'user'},
                           'view': 'sa_home'},
                          {'visible': True, 'name': 'user', 'param': {'name': 'user'},
                           'view': 'sa_list'},
                          {'visible': False, 'name': 'create', 'param': {'name': 'user'},
                           'view': 'sa_list'}]
                         )
        self.assertEqual(responce['sa_crud']['table'], User)
