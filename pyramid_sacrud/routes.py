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
from .common import pkg_prefix
from .resources import GroupResource
from pyramid.events import ApplicationCreated


def admin_factory(request):
    models = request.registry.settings[CONFIG_RESOURCES]
    return {
        str(group): GroupResource(group, resources)
        for group, resources in models
    }


def resources_preparing(app):
    """ Wrap all resources in settings.
    """
    settings = app.app.registry.settings
    resources = settings.get(CONFIG_RESOURCES, None)
    if not resources:
        return

    def wrapper(resource, parent):
        if not getattr(resource, '__parent__', False):
            resource.__parent__ = parent
        return resource

    models = [(k, [wrapper(r, GroupResource(k, v)) for r in v])
              for k, v in resources]
    settings[CONFIG_RESOURCES] = models


def includeme(config):
    config.add_subscriber(resources_preparing, ApplicationCreated)
    prefix = pkg_prefix(config)
    config.add_route(PYRAMID_SACRUD_HOME, prefix)
    config.add_route(PYRAMID_SACRUD_VIEW, '/*traverse', factory=admin_factory)
    config.add_request_method(
        lambda x: prefix or config.route_prefix, 'sacrud_prefix',
        reify=True, property=True
    )
