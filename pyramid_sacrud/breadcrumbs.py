#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Breadcrumbs for sacrud pyramid extension.
"""


def get_crumb(name, visible, view, params):
    crumb = name
    if isinstance(name, dict):
        """ {'category_id': 1, 'group_id': 1}
        to
            category_id=1, group_id=1
        """
        crumb = ""
        for k, v in name.iteritems():
            crumb = crumb + " " + k + "=" + v + ","
        crumb = crumb[:-1]

    return {'name': crumb, 'visible': visible, 'view': view, 'param': params}


def breadcrumbs(tname, view, id=None):
    bc = {}
    bc['sa_list'] = [get_crumb('Dashboard', True, 'sa_home', {'table': tname}),
                     get_crumb(tname, True, 'sa_list', {'table': tname})]

    bc['sa_create'] = bc['sa_list'] +\
        [get_crumb('create', False, 'sa_list', {'table': tname})]

    bc['sa_read'] = bc['sa_update'] = bc['sa_list'] +\
        [get_crumb(id, False, 'sa_list', {'table': tname})]

    bc['sa_union'] = bc['sa_list'] +\
        [get_crumb('union', False, 'sa_list', {'table': tname})]

    return bc[view]
