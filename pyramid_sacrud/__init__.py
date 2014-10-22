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

import sqlalchemy
import sqlalchemy.orm as orm
from zope.sqlalchemy import ZopeTransactionExtension

from .common import _silent_none, pkg_prefix


def add_routes(config):
    prefix = pkg_prefix(config)
    config.add_route('sa_home',           prefix)
    config.add_route('sa_list',           prefix + '{table}')
    config.add_route('sa_create',         prefix + '{table}/create')
    config.add_route('sa_update',         prefix + '{table}/update/*pk')
    config.add_route('sa_delete',         prefix + '{table}/delete/*pk')


def add_jinja2(config):
    config.include('pyramid_jinja2')
    config.commit()
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.finalize = _silent_none
    config.add_jinja2_search_path("pyramid_sacrud:templates")
    config.add_jinja2_extension('jinja2.ext.loopcontrols')


def add_database(config):
    engine = sqlalchemy.engine_from_config(config.registry.settings)
    DBSession = orm.scoped_session(
        orm.sessionmaker(extension=ZopeTransactionExtension()))
    DBSession.configure(bind=engine)
    config.set_request_property(lambda x: DBSession, 'dbsession', reify=True)


def includeme(config):

    add_database(config)
    add_jinja2(config)

    # Routes
    config.include(add_routes)

    # Assets
    config.include('pyramid_sacrud.assets')

    # Static
    config.add_static_view('sa_static', 'pyramid_sacrud:static')
    config.add_static_view('sa_deform_static', 'deform:static')
    config.add_static_view('sa_elfinder_static', 'pyramid_elfinder:static')
    config.scan()
