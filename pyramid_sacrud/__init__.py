#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Includeme of SACRUD
"""

CONFIG_RESOURCES = 'pyramid_sacrud.models'
CONFIG_DASHBOARD_ROW_LEN = 'pyramid_sacrud.dashboard_row_len'
PYRAMID_SACRUD_HOME = 'pyramid_sacrud_home'
PYRAMID_SACRUD_VIEW = 'pyramid_sacrud_view'
HOME_VIEW_TEMPLATE = '/sacrud/home.jinja2'


def includeme(config):
    config.include('.localization')
    config.include('.assets')
    config.include('.routes')
    config.scan('.views')
