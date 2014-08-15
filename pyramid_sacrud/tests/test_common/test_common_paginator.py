#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Test for sacrud.common
"""

import unittest

from pyramid.testing import DummyRequest
from webhelpers.paginate import PageURL_WebOb

from pyramid_sacrud.common.paginator import get_current_page, get_paginator


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.request = DummyRequest()

    def tearDown(self):
        pass


class PaginatorTest(BaseTest):

    def test_get_current_page(self):
        page = get_current_page(self.request)
        self.assertEqual(page, 1)
        self.request.GET['page'] = 5
        page = get_current_page(self.request)
        self.assertEqual(page, 5)

    def test_get_paginator(self):
        paginator = get_paginator(self.request)
        self.assertEqual(paginator['items_per_page'], 10)
        self.assertEqual(paginator['page'], 1)
        self.assertEqual(type(paginator['url']), PageURL_WebOb)

        self.request.GET['page'] = 100500
        paginator = get_paginator(self.request, 20)
        self.assertEqual(paginator['items_per_page'], 20)
        self.assertEqual(paginator['page'], 100500)
        self.assertEqual(type(paginator['url']), PageURL_WebOb)
