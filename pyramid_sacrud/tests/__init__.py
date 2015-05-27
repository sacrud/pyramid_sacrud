#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Tests of pyramid_sacrud
"""
import os
import unittest

from .models import DATABASE_FILE, Session


class AppTest(unittest.TestCase):
    pass


class TransactionalTest(AppTest):
    """
    Run tests against a relational database within a transactional boundary.
    """

    def setUp(self):
        super(TransactionalTest, self).setUp()
        from .models import engine
        self.connection = engine.connect()
        self.transaction = self.connection.begin()
        self.session = Session()

    def tearDown(self):
        Session.remove()
        self.transaction.rollback()
        self.connection.close()
        self.session.close()
        os.remove(DATABASE_FILE)
        super(TransactionalTest, self).tearDown()
