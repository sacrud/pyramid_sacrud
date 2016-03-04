#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""Docker Web interface"""

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from resources import Image


def main(global_settings, **settings):
    """Entrypoint for WSGI app."""
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    # Add session engine
    config = Configurator(
        settings=settings,
        session_factory=my_session_factory
    )
    # Add static and templates
    config.add_static_view(name='static', path='static')
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('templates')
    config.include('ps_crud')

    # Setting up pyramid_sacrud
    config.include('pyramid_sacrud', route_prefix='admin')
    settings = config.get_settings()
    settings['pyramid_sacrud.models'] = (
        ('Docker', [Image(), ]),
    )

    # Make app
    config.scan('views')
    return config.make_wsgi_app()


if __name__ == '__main__':
    settings = {
        'pyramid.includes': 'pyramid_debugtoolbar'
    }
    app = main({}, **settings)

    from waitress import serve
    serve(app, host='0.0.0.0', port=6543)
