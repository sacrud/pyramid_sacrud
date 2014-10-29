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

from pyramid_sacrud.common.paginator import get_current_page, get_paginator


class PaginatorTest(unittest.TestCase):

    def test_get_current_page(self):
        request = DummyRequest()
        page = get_current_page(request)
        self.assertEqual(page, 1)
        request.GET['page'] = 5
        page = get_current_page(request)
        self.assertEqual(page, 5)

    def test_get_paginator(self):
        request = DummyRequest()
        paginator = get_paginator(request)
        self.assertEqual(paginator['items_per_page'], 10)
        self.assertEqual(paginator['page'], 1)

        request.GET['page'] = 100500
        paginator = get_paginator(request, 20)
        self.assertEqual(paginator['items_per_page'], 20)
        self.assertEqual(paginator['page'], 100500)
