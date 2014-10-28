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
    if 'verbose_name' in column.info:
        return column.info['verbose_name']
    if column.name:
        return column.name
    if isinstance(column, str):
        return column
    return ''


def widget(fun):
    def wrapped(*args, **kwargs):
        sacrud_name = ''
        params = {}
        if 'column' in kwargs:
            if hasattr(kwargs['column'], 'property'):
                sacrud_name = kwargs['column'].property.key
            params.update({'column': kwargs['column']})
        if 'sacrud_name' in kwargs:
            sacrud_name = kwargs['sacrud_name']
        params.update({'sacrud_name': sacrud_name, 'name': sacrud_name})
        response = fun(*args, **kwargs)
        params.update(response)
        return params
    return wrapped


@widget
def widget_link(*args, **kwargs):
    return {'info': {'sacrud_position': 'inline',
                     'sacrud_list_template': 'sacrud/custom/WidgetLinkList.jinja2',
                     },
            'name': get_name(kwargs['column']),
            }


@widget
def widget_row_lambda(*args, **kwargs):
    return {
        'name': kwargs['name'],
        'info': {
            'sacrud_position': 'inline',
            'sacrud_list_content': kwargs['content'],
        },
    }


class Widget(object):
    def __init__(self, column, name=''):
        self.column = column
        self.info = {'verbose_name': name,
                     'name': name}


class WidgetM2M(Widget):
    def __init__(self, column, name=''):
        super(WidgetM2M, self).__init__(column, name='')
