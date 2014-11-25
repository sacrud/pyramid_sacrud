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
from ..common import pkg_prefix


def includeme(config):
    prefix = pkg_prefix(config)
    config.add_route('sa_home',   prefix + '/')
    config.add_route('sa_list',   prefix + '{table}/')
    config.add_route('sa_create', prefix + '{table}/create/')
    config.add_route('sa_update', prefix + '{table}/update/*pk')
    config.add_route('sa_delete', prefix + '{table}/delete/*pk')
