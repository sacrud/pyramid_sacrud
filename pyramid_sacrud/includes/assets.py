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
from ..common import _silent_none


def add_jinja2(config):
    config.include('pyramid_jinja2')
    config.commit()
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.finalize = _silent_none
    config.add_jinja2_search_path("pyramid_sacrud:templates")
    config.add_jinja2_extension('jinja2.ext.loopcontrols')


def includeme(config):
    config.include(add_jinja2)
    config.include('sacrud_deform')
    config.add_static_view('deform_static', 'deform:static')
    config.add_static_view('sa_static', 'pyramid_sacrud:static')
    config.add_static_view('sa_elfinder_static', 'pyramid_elfinder:static')
