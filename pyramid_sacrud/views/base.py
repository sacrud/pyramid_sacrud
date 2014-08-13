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
from collections import OrderedDict

from pyramid.view import view_config

from ..common import get_settings_param


def sorted_dashboard_widget(tables, dashboard_columns=3, session=None,
                            model=None):
    def get_position(name):
        if model and session:
            return session.query(model).filter_by(widget=(name or None)).one().position
        return tables[name]['position']

    def set_position(name, value):
        value['position'] = get_position(name)
        return value

    def getKey(item):
        position = item[1]['position']
        key = position % dashboard_columns
        if not key:
            key = dashboard_columns
        return (key, position)

    dashboard_widget = {k: set_position(k, v) for k, v in tables.iteritems()}
    return OrderedDict(sorted(dashboard_widget.iteritems(),
                              cmp=lambda t1, t2: cmp(getKey(t1), getKey(t2))))


@view_config(route_name='sa_home', renderer='/sacrud/home.jinja2')
def sa_home(request):
    session = request.dbsession
    tables = get_settings_param(request, 'pyramid_sacrud.models')
    dashboard_columns = request.registry.settings\
        .get('sacrud_dashboard_columns', 3)
    dashboard_model = request.registry.settings.get('sacrud_dashboard_position_model', None)
    return {'dashboard_columns': dashboard_columns,
            'tables': sorted_dashboard_widget(tables, dashboard_columns,
                                              session, dashboard_model)
            }
