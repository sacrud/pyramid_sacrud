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
from pyramid.events import ApplicationCreated

from . import CONFIG_MODELS, PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_VIEW
from .common import pkg_prefix


class GroupResource(object):

    def __init__(self, group, resources):
        self.group = group
        self.resources = resources

    def __getitem__(self, name):
        for resource in self.resources:
            if resource.__name__ == name:
                resource.parent = self
                return resource

    @property
    def __name__(self):
        return str(self.group)


def admin_factory(request):
    models = request.registry.settings['pyramid_sacrud.models']
    return {
        str(group): GroupResource(group, value)
        for group, value in models
    }


def models_preparing(app):
    settings = app.app.registry.settings
    models = settings[CONFIG_MODELS]

    def set_parent(resource, parent):
        resource.parent = parent
        return resource
    models = [(k, [set_parent(r, GroupResource(k, v)) for r in v])
              for k, v in models]
    settings[CONFIG_MODELS] = models


def includeme(config):
    config.add_subscriber(models_preparing, ApplicationCreated)

    prefix = pkg_prefix(config)
    config.add_route(PYRAMID_SACRUD_HOME, prefix)
    config.add_route(PYRAMID_SACRUD_VIEW, '/*traverse', factory=admin_factory)
    config.add_request_method(
        lambda x: config.route_prefix, 'sacrud_prefix',
        reify=True, property=True
    )
