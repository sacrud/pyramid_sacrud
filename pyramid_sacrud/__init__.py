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
import os

import sqlalchemy
import sqlalchemy.orm as orm
from webassets import Bundle
from zope.sqlalchemy import ZopeTransactionExtension

from .common import _silent_none, pkg_prefix


def add_routes(config):
    prefix = pkg_prefix(config)
    config.add_route('sa_home',           prefix)
    config.add_route('sa_list',           prefix + '{table}')
    config.add_route('sa_create',         prefix + '{table}/create')
    config.add_route('sa_update',         prefix + '{table}/update/*pk')
    config.add_route('sa_delete',         prefix + '{table}/delete/*pk')


def webassets_init(config):
    curdir = os.path.dirname(os.path.abspath(__file__))
    settings = config.registry.settings
    settings["webassets.base_dir"] = os.path.join(curdir, 'static')
    settings["webassets.base_url"] = "/%s/sa_static" % config.route_prefix
    settings["webassets.debug"] = "True"
    settings["webassets.updater"] = "timestamp"
    settings["webassets.jst_compiler"] = "Handlebars.compile"
    settings["webassets.url_expire"] = "False"
    settings["webassets.static_view"] = "True"
    settings["webassets.cache_max_age"] = 3600

    config.include('pyramid_webassets')

    config.add_jinja2_extension('webassets.ext.jinja2.AssetsExtension')
    assets_env = config.get_webassets_env()
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.assets_environment = assets_env


def add_css_webasset(config):
    settings = config.registry.settings
    css_file = os.path.join(settings["webassets.base_dir"], 'css', '_base.css')
    css_bundle = Bundle('css/*.css', 'css/**/*.css',
                        filters='cssmin')
    if settings.get('sacrud.debug', False):
        css_bundle = Bundle(css_bundle,  # pragma: no cover
                            Bundle('styl/*.styl', 'styl/**/*.styl',
                                   filters=['stylus', 'cssmin'],
                                   output=css_file,
                                   ),
                            )
    config.add_webasset('sa_css', css_bundle)


def add_js_webasset(config):
    from shutil import copyfile                                     # pragma: no cover
    settings = config.registry.settings                             # pragma: no cover
    js_folder = os.path.join(settings["webassets.base_dir"], 'js')  # pragma: no cover

    bower = ["jquery/dist/jquery.min.js",                           # pragma: no cover
             "chosen/public/chosen.jquery.min.js",
             "jquery-ui/ui/minified/jquery-ui.min.js",
             "speakingurl/speakingurl.min.js",
             "jqueryui-timepicker-addon/src/jquery-ui-timepicker-addon.js",
             "requirejs/require.js",
             "elfinder/src/elfinder/js/elfinder.js",
             "jquery-maskedinput/dist/jquery.maskedinput.min.js",
             ]
    for f in bower:                                                 # pragma: no cover
        src = os.path.join(js_folder, 'bower_components', f)        # pragma: no cover
        dst = os.path.join(js_folder, 'lib', f.split('/')[-1])      # pragma: no cover
        copyfile(src, dst)                                          # pragma: no cover


def includeme(config):
    engine = sqlalchemy.engine_from_config(config.registry.settings)
    DBSession = orm.scoped_session(
        orm.sessionmaker(extension=ZopeTransactionExtension()))
    DBSession.configure(bind=engine)
    config.set_request_property(lambda x: DBSession, 'dbsession', reify=True)

    # Dashboard widget
    settings = config.registry.settings

    # Jinja2
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.finalize = _silent_none
    config.add_jinja2_search_path("pyramid_sacrud:templates")
    config.add_jinja2_extension('jinja2.ext.loopcontrols')

    # Routes
    config.include(add_routes)
    config.add_static_view('sa_static', 'pyramid_sacrud:static')

    # Assets
    config.add_static_view('sa_deform_static',
                           'deform:static')

    config.include(webassets_init)
    config.include(add_css_webasset)
    if settings.get('sacrud.debug', False):
        config.include(add_js_webasset)  # pragma: no cover

    config.scan()
