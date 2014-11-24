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
from sacrud import action


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
        self.name = name
        self.info = self.get_info({})

    def get_info(self, value):
        base = {'verbose_name': self.name,
                'name': self.name}
        return dict(list(base.items()) +
                    list(value.items()))

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
        self.info = self.get_info({})
        self.table = table
        self.relation = relation


class WidgetInlines(Widget):

    def __init__(self, relation, table, schema, name=''):
        self.name = name
        self.info = self.get_info({})
        self.table = table
        self.schema = schema
        self.relation = relation
        self.remote_side = list(self.relation.property.remote_side)

    def preprocessing(self, obj=None):
        """ Add linked values of obj to form inlines.
        """
        schema = self.schema()
        if obj:
            fstruct = schema.flatten(schema)
            appstruct = schema.unflatten(fstruct)
            key = appstruct.popitem()[0][:-2]
            values = []
            for item in getattr(obj, key) or ():
                values.append(item.__dict__)
            schema.children[0].default = values
        return schema

    def postprocessing(self, obj, session, request):
        """ CREATE or UPDATE inline rows before save obj.
        """
        # XXX: rewrite it
        # TODO: add to docs WidgetInlines
        values = request[self.relation.key+'[]']
        for value in values:
            for rs in self.remote_side:
                pk = list(rs.foreign_keys)[0].column
                value[rs.name] = getattr(obj, pk.name)
            action.CRUD(session, self.table, request=value).add(commit=False)


class WidgetRowLambda(Widget):

    def __init__(self, function, name=''):
        self.name = name
        self.function = function
        info = {
            'sacrud_position': 'inline',
            'sacrud_list_content': function,
        }
        self.info = self.get_info(info)
