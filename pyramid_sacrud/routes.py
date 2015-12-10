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

from . import CONFIG_MODELS, PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_VIEW
from .common import pkg_prefix
from .resources import GroupResource


def admin_factory(request):
    models = request.registry.settings[CONFIG_MODELS]
    return {
        str(group): GroupResource(group, resources)
        for group, resources in models
    }


def includeme(config):
    prefix = pkg_prefix(config)
    config.add_route(PYRAMID_SACRUD_HOME, prefix)
    config.add_route(PYRAMID_SACRUD_VIEW, '/*traverse', factory=admin_factory)
    config.add_request_method(
        lambda x: prefix or config.route_prefix, 'sacrud_prefix',
        reify=True, property=True
    )
