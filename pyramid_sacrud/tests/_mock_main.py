#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
main function for functional test module
"""
from pyramid.config import Configurator

from .models.auth import Profile, User, Groups


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')

    # SACRUD
    config.include('pyramid_sacrud', route_prefix='/admin')
    settings = config.registry.settings
    settings['pyramid_sacrud.models'] = (
        ('', [User]),
        ('Auth models', [User, Profile, Groups])
    )
    return config.make_wsgi_app()
