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
from pyramid.events import BeforeRender, subscriber
from pyramid.view import view_config

from .. import CONFIG_DASHBOARD_ROW_LEN
from ..common import get_models_from_settings, get_settings_param
from ..security import (PYRAMID_SACRUD_CREATE, PYRAMID_SACRUD_DELETE,
                        PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_LIST,
                        PYRAMID_SACRUD_UPDATE)

HOME_TEMPLATE = '/sacrud/home.jinja2'
CREATE_TEMPLATE = '/sacrud/create.jinja2'
UPDATE_TEMPLATE = CREATE_TEMPLATE
LIST_TEMPLATE = '/sacrud/list.jinja2'

SACRUD_LIST_TEMPLATE = 'sacrud_list_template'
SACRUD_EDIT_TEMPLATE = 'sacrud_edit_template'


@subscriber(BeforeRender)
def add_global(event):
    event['PYRAMID_SACRUD_HOME'] = PYRAMID_SACRUD_HOME
    event['PYRAMID_SACRUD_LIST'] = PYRAMID_SACRUD_LIST
    event['PYRAMID_SACRUD_CREATE'] = PYRAMID_SACRUD_CREATE
    event['PYRAMID_SACRUD_DELETE'] = PYRAMID_SACRUD_DELETE
    event['PYRAMID_SACRUD_UPDATE'] = PYRAMID_SACRUD_UPDATE


@view_config(
    renderer=HOME_TEMPLATE,
    route_name=PYRAMID_SACRUD_HOME,
    permission=PYRAMID_SACRUD_HOME)
def sa_home(request):
    tables = get_models_from_settings(request)
    dashboard_row_len = get_settings_param(request, CONFIG_DASHBOARD_ROW_LEN)
    return {'dashboard_row_len': int(dashboard_row_len or 3),
            'tables': tables}
