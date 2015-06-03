#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Routes for pyramid_sacrud
"""
from ..common import pkg_prefix
from ..security import (PYRAMID_SACRUD_CREATE, PYRAMID_SACRUD_DELETE,
                        PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_LIST,
                        PYRAMID_SACRUD_UPDATE)


def includeme(config):
    prefix = pkg_prefix(config)
    config.add_route(PYRAMID_SACRUD_HOME, prefix)
    config.add_route(PYRAMID_SACRUD_LIST, prefix + '{table}/')
    config.add_route(PYRAMID_SACRUD_CREATE, prefix + '{table}/create/')
    config.add_route(PYRAMID_SACRUD_UPDATE, prefix + '{table}/update/*pk')
    config.add_route(PYRAMID_SACRUD_DELETE, prefix + '{table}/delete/*pk')
