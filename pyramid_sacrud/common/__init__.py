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
import sqlalchemy
from sacrud.common import get_attrname_by_colname


def import_from_string(path):
    if not isinstance(path, str):
        return path
    parts = path.split(':')
    temp = __import__(parts[0], globals(), locals(), [parts[1], ], 0)
    return getattr(temp, parts[1], None)


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
    """
    >>> _silent_none(0)
    0
    >>> _silent_none('foo')
    'foo'
    >>> _silent_none(None)
    ''
    >>> _silent_none('None')
    ''
    >>> _silent_none(False)
    ''
    >>> class Foo(object):
    ...   def __bool__(self):
    ...     return False
    >>> _silent_none(Foo)
    <class 'pyramid_sacrud.common.Foo'>
    >>> _silent_none(u'ПревеД!')
    u'\\xd0\\x9f\\xd1\\x80\\xd0\\xb5\\xd0\\xb2\\xd0\\xb5\\xd0\\x94!'
    """
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


def set_jinja2_silent_none(config):
    """ if variable is None print '' instead of 'None'
    """
    config.commit()
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.finalize = _silent_none


def get_settings_param(request, name):
    settings = request.registry.settings
    return settings[name]


def get_obj_from_settings(request, name):
    settings = request
    if not isinstance(request, dict):
        settings = request.registry.settings
    position_model = settings.get(name)
    if isinstance(position_model, str):
        return import_from_string(position_model)
    return position_model


def sacrud_env(fun):
    jinja2_globals = {'str': str, 'getattr': getattr, 'isinstance': isinstance,
                      'get_attrname_by_colname': get_attrname_by_colname,
                      'hasattr': hasattr,
                      'sqlalchemy': sqlalchemy}

    def wrapped(*args, **kwargs):
        response = fun(*args, **kwargs)
        if hasattr(response, 'update'):
            DBSession = {'session': args[0].request.dbsession}
            response.update(jinja2_globals)
            response.update(DBSession)
        return response
    return wrapped
