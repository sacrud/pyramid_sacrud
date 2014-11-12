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

    @property
    def info(self):
        return {'verbose_name': self.name,
                'name': self.name}

    def preprocessing(self, *args, **kwargs):
        """ Run when show form. GET method
        """
        pass

    def postprocessing(self, *args, **kwargs):
        """ Run after submit form. POST method
        """
        pass


class WidgetRelationship(Widget):

    def __init__(self, relation, table, name=''):
        self.name = name
        self.table = table
        self.relation = relation


class WidgetInlines(Widget):

    def __init__(self, relation, table, schema, name=''):
        self.name = name
        self.table = table
        self.relation = relation
        self.schema = schema

    def preprocessing(self, obj=None):
        """ Add linked values of obj to form inlines.
        """
        pass

    def postprocessing(self, obj, session, request):
        """ CREATE or UPDATE inline rows before save obj.
        """
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT


class WidgetRowLambda(Widget):

    def __init__(self, function, name=''):
        self.name = name
        self.info.update({
            'sacrud_position': 'inline',
            'sacrud_list_content': function,
        })
