#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Any helpers for Pyramid
"""
import colander
import sqlalchemy


def preprocessing_value(key, value, form):
    for groups in form.children:
        for column in groups:
            if column.name == key:
                if not str(value).isdigit() and isinstance(
                        column.typ,
                        (colander.Int, colander.Integer,
                         colander.Float, colander.Decimal)):
                    value = sqlalchemy.sql.null()
                elif value is colander.null:
                    value = ""
                return value


def pkg_prefix(config):
    '''
    Function for return pkg prefix.

    >>> from pyramid.config import Configurator
    >>> settings = {'foo': 'foo', 'bar': 'bar'}

    # Create config
    >>> config = Configurator(settings=settings)

    # w/o route_prefix
    >>> pkg_prefix(config)
    '/sacrud/'

    # with route_prefix
    >>> config.route_prefix = "/admin"
    >>> pkg_prefix(config)
    ''
    '''
    return '' if config.route_prefix else '/sacrud/'


def _silent_none(value):
    if type(value) == int:
        return value
    if hasattr(value, '__bool__'):
        return value
    if not value:
        return ''
    try:
        if str(value) == 'None':
            return ''
    except UnicodeEncodeError:
        pass
    return value


def set_jinja2_silent_none(config):  # pragma: no cover
    """ if variable is None print '' instead of 'None'
    """
    config.commit()
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.finalize = _silent_none
