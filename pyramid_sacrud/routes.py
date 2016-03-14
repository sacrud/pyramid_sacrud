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

from . import CONFIG_RESOURCES, PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_VIEW
from .resources import GroupResource
from pyramid.events import ApplicationCreated


def admin_factory(request):
    config = request.registry.settings[CONFIG_RESOURCES]
    return {
        str(group): GroupResource(group, resources)
        for group, resources in config
    }


def resources_preparing_factory(app, wrapper):
    """ Factory which wrap all resources in settings.
    """
    settings = app.app.registry.settings
    config = settings.get(CONFIG_RESOURCES, None)
    if not config:
        return

    resources = [(k, [wrapper(r, GroupResource(k, v)) for r in v])
                 for k, v in config]
    settings[CONFIG_RESOURCES] = resources


def resources_preparing(app):

    def wrapper(resource, parent):
        if not getattr(resource, '__parent__', False):
            resource.__parent__ = parent
        return resource

    resources_preparing_factory(app, wrapper)


def includeme(config):
    config.add_subscriber(resources_preparing, ApplicationCreated)
    if not config.route_prefix:
        config.route_prefix = 'sacrud'
    config.add_route(PYRAMID_SACRUD_HOME, '/')
    config.add_route(PYRAMID_SACRUD_VIEW, '/*traverse', factory=admin_factory)
    config.add_request_method(
        lambda x: config.route_prefix, 'sacrud_prefix',
        reify=True, property=True
    )
