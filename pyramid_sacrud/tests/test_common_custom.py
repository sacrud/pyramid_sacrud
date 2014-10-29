#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Test for sacrud.common.custom
"""
import unittest

from pyramid_sacrud.common.custom import get_name, widget_link
from pyramid_sacrud.tests.models.auth import User


class CustomTest(unittest.TestCase):

    def test_get_name(self):
        self.assertEqual('sex', get_name(User.sex))
        self.assertEqual('id', get_name(User.id))
        self.assertEqual('user password', get_name(User.password))

        class EmptyType: pass
        foo = EmptyType()
        foo.info = {}
        foo.name = ''
        self.assertEqual('', get_name(foo))

    def test_widget_link(self):
        link = widget_link(column=User.sex)
        self.assertEqual(link['info'],
                         {'sacrud_list_template': 'sacrud/custom/WidgetLinkList.jinja2',
                          'sacrud_position': 'inline'})
        self.assertEqual(link['column'], User.sex)
        self.assertEqual(link['name'], 'sex')
        self.assertEqual(link['sacrud_name'], 'sex')

        link = widget_link(column=User.sex, sacrud_name=u'foo bar баз')
        self.assertEqual(link['info'],
                         {'sacrud_list_template': 'sacrud/custom/WidgetLinkList.jinja2',
                          'sacrud_position': 'inline'})
        self.assertEqual(link['column'], User.sex)
        self.assertEqual(link['name'], 'sex')
        self.assertEqual(link['sacrud_name'], u'foo bar \u0431\u0430\u0437')
