#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Views for Pyramid frontend
"""
from pyramid.view import view_config
from pyramid.events import subscriber, BeforeRender
from pyramid.location import lineage

from . import (
    CONFIG_RESOURCES,
    HOME_VIEW_TEMPLATE,
    PYRAMID_SACRUD_HOME,
    CONFIG_DASHBOARD_ROW_LEN
)


@subscriber(BeforeRender)
def add_global_params(event):
    event['getattr'] = getattr
    event['lineage'] = lineage
    event['PYRAMID_SACRUD_HOME'] = PYRAMID_SACRUD_HOME


@view_config(
    renderer=HOME_VIEW_TEMPLATE,
    route_name=PYRAMID_SACRUD_HOME,
    permission=PYRAMID_SACRUD_HOME)
def home_view(request):
    settings = request.registry.settings
    dashboard_row_len = int(settings.get(CONFIG_DASHBOARD_ROW_LEN, 3))
    return {'dashboard_row_len': dashboard_row_len,
            'resources': settings.get(CONFIG_RESOURCES, None)}
