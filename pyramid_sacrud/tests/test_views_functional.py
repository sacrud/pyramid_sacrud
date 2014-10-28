#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Functional tests for views
"""
from webtest import TestApp

from .models import TEST_DATABASE_CONNECTION_STRING
from .mock_main import main
from .test_views import _TransactionalFixture


class PyramidApp(_TransactionalFixture):
    def setUp(self):
        super(PyramidApp, self).setUp()
        settings = {'sqlalchemy.url': TEST_DATABASE_CONNECTION_STRING}
        app = main({}, **settings)
        self.testapp = TestApp(app)


class HomeFuncTests(PyramidApp):

    def test_sa_home(self):
        res = self.testapp.get('/admin/', status=200)
        self.failUnless('Auth models' in str(res.body))
        self.failUnless('user' in str(res.body))
        self.failUnless('profile' in str(res.body))


class CreateFuncTests(PyramidApp):
    pass
