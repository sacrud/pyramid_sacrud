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
from pyramid import testing

from . import TransactionalTest
from ..views import sa_home
from .models.account import Account, Transaction

# from .models import Session


class _TransactionalFixture(TransactionalTest):

    def _client_fixture(self):
        pass
        # client = Client(identifier='12345', secret="some secret")
        # Session.add(client)
        # return client

    def _init_pyramid_sacrud_settings(self, request):
        settings = request.registry.settings
        settings['pyramid_sacrud.models'] =\
            {
                'Permissions': {
                    'tables': (
                        Account,
                    ),
                    'position': 1,
                },
                'Users': {
                    'tables': (
                        Transaction,
                    ),
                    'position': 4,
                }
            }


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
        self.assertEquals(responce['widgets'][0].tables, (Account,))
        self.assertEquals(responce['widgets'][0].position, 1)
        self.assertEquals(responce['widgets'][1].tables, [])
        self.assertEquals(responce['widgets'][2].tables, [])
        self.assertEquals(responce['widgets'][3].tables, (Transaction,))
        self.assertEquals(responce['widgets'][3].position, 4)
