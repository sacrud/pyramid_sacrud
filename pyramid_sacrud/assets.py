#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
"""
Assets
"""


def includeme(config):
    config.add_static_view('sa_static', 'pyramid_sacrud:static')
    config.add_static_view('sa_deform_static', 'deform:static')
