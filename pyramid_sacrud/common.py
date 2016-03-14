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
try:
    from types import BooleanType as bool  # noqa
except ImportError:
    pass


def _silent_none(value):
    '''
    >>> _silent_none(12)
    12
    >>> _silent_none(True)
    True
    >>> _silent_none(None)
    ''
    >>> _silent_none('')
    ''
    >>> _silent_none(False)
    False
    >>> _silent_none('None')
    ''
    >>> _silent_none("foooooooo")
    'foooooooo'
    '''
    if value is None:
        return ''
    if type(value) == int:
        return value
    if type(value) == bool:
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
