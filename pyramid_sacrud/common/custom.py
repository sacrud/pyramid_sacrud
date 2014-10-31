#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Any instruments for customizing Models
"""


def get_name(column):
    if isinstance(column, str):
        return column
    if 'verbose_name' in column.info:
        return column.info['verbose_name']
    if column.name:
        return column.name
    return ''


class Widget(object):
    def __init__(self, name=''):
        self.info = {'verbose_name': name,
                     'name': name}


class WidgetRelationship(Widget):
    def __init__(self, relation, table=None, name=''):
        super(WidgetRelationship, self).__init__(name=name)
        self.table = table
        self.relation = relation


class WidgetRowLambda(Widget):
    def __init__(self, function, name=''):
        super(WidgetRowLambda, self).__init__(name=name)
        self.info.update({
            'sacrud_position': 'inline',
            'sacrud_list_content': function,
        })
