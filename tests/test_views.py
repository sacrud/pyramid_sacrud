#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

from pyramid import testing
from pyramid_sacrud import CONFIG_RESOURCES
from pyramid_sacrud.views import home_view


class Foo:
    pass


class TestHome(object):

    def test_no_models(self):
        request = testing.DummyRequest()
        request.registry.settings = {}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': None}

    def test_empty_of_models(self):
        request = testing.DummyRequest()
        request.registry.settings = {CONFIG_RESOURCES: None}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': None}

    def test_empty_list_of_models(self):
        request = testing.DummyRequest()
        request.registry.settings = {CONFIG_RESOURCES: []}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': []}

    def test_with_models(self):
        request = testing.DummyRequest()
        request.registry.settings = {CONFIG_RESOURCES: [("foo", Foo)]}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': [("foo", Foo)]}

    def test_unicode_group_name(self):
        request = testing.DummyRequest()
        request.registry.settings = {CONFIG_RESOURCES: [("говядо", Foo)]}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': [("говядо", Foo)]}
        request.registry.settings = {CONFIG_RESOURCES: [(u"говядо", Foo)]}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': [(u"говядо", Foo)]}
        request.registry.settings = {CONFIG_RESOURCES: [
            (u'\u0433\u043e\u0432\u044f\u0434\u043e', Foo)
        ]}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': [(u"говядо", Foo)]}


class TestHomeFunc(object):

    def test_200(self, testapp):
        testapp.get('/sacrud/', status=200)
        assert True
