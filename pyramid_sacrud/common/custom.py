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


class WidgetRowLambda(Widget):

    def __init__(self, function, name=''):
        self.name = name
        self.function = function
        info = {
            'sacrud_position': 'inline',
            'sacrud_list_content': function,
        }
        self.info = self.get_info(info)
