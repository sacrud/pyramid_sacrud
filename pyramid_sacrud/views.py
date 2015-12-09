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
    CONFIG_MODELS,
    HOME_VIEW_TEMPLATE,
    PYRAMID_SACRUD_HOME,
    CONFIG_DASHBOARD_ROW_LEN
)
from .common import get_settings_param


@subscriber(BeforeRender)
def add_global_params(event):
    event['lineage'] = lineage
    event['PYRAMID_SACRUD_HOME'] = PYRAMID_SACRUD_HOME


@view_config(
    renderer=HOME_VIEW_TEMPLATE,
    route_name=PYRAMID_SACRUD_HOME,
    permission=PYRAMID_SACRUD_HOME)
def home_view(request):
    resources = request.registry.settings[CONFIG_MODELS]
    dashboard_row_len = get_settings_param(request, CONFIG_DASHBOARD_ROW_LEN)
    return {'dashboard_row_len': int(dashboard_row_len or 3),
            'resources': resources}
