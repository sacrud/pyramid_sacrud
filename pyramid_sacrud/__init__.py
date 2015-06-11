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

CONFIG_MODELS = 'pyramid_sacrud.models'
CONFIG_DASHBOARD_ROW_LEN = 'pyramid_sacrud.dashboard_row_len'


def includeme(config):
    config.include('.includes')
    config.scan('.views')
