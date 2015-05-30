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
from .includes.localization import _ps
from .security import (PYRAMID_SACRUD_CREATE, PYRAMID_SACRUD_HOME,
                       PYRAMID_SACRUD_LIST, PYRAMID_SACRUD_UPDATE)


def get_crumb(name, visible, view, params):
    crumb = name
    if isinstance(name, dict):
        """ {'category_id': 1, 'group_id': 1}
        to
            category_id=1, group_id=1
        """
        crumb = ""
        for k, v in name.items():
            crumb = crumb + " " + k + "=" + v + ","
        crumb = crumb[:-1]

    return {'name': crumb, 'visible': visible, 'view': view, 'param': params}


def breadcrumbs(name, verbose, view, id=None):
    bc = {}
    bc[PYRAMID_SACRUD_LIST] = [
        get_crumb(_ps('Dashboard'), True, PYRAMID_SACRUD_HOME, {'name': name}),
        get_crumb(verbose, True, PYRAMID_SACRUD_LIST, {'name': name})]

    bc[PYRAMID_SACRUD_CREATE] = bc[PYRAMID_SACRUD_LIST] +\
        [get_crumb('create', False, PYRAMID_SACRUD_LIST, {'name': name})]

    bc[PYRAMID_SACRUD_UPDATE] = bc[PYRAMID_SACRUD_LIST] +\
        [get_crumb(id, False, PYRAMID_SACRUD_LIST, {'name': name})]

    return bc[view]
