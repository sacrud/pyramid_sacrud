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

from ..common import get_settings_param


def sorted_dashboard_widget(tables):
    class DashboardWidget(object):
        def __init__(self, name, **kwargs):
            self.name = name
            self.tables = kwargs['tables']
            self.position = kwargs['position']
    widgets = []
    for k, v in tables.items():
        widgets.append(DashboardWidget(name=k, **v))
        widgets = sorted(widgets, key=lambda x: x.position)
    for i, widget in enumerate(widgets[:-1]):
        delta = widgets[i+1].position - widget.position
        for x in range(delta-1):
            widgets.insert(i+1, DashboardWidget('', tables=[], position=i+x+2))
    return widgets


@view_config(route_name='sa_home', renderer='/sacrud/home.jinja2',
             permission='pyramid_sacrud_home')
def sa_home(request):
    tables = get_settings_param(request, 'pyramid_sacrud.models')
    dashboard_columns = request.registry.settings\
        .get('sacrud_dashboard_columns', 3)
    return {'dashboard_columns': dashboard_columns,
            'widgets': sorted_dashboard_widget(tables)
            }
