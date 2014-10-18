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
import os
from shutil import copyfile

from webassets import Bundle


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


def add_css_assets(config):
    settings = config.registry.settings
    css_file = os.path.join(
        settings["webassets.base_dir"], 'css', '__main.css')
    css_bundle = Bundle(
        'css/*.css',
        'css/**/*.css',
        filters='cssmin', output=css_file)
    # if settings.get('sacrud.debug_css', False):
    #     css_bundle = Bundle(css_bundle,                   # pragma: no cover
    #                         Bundle(
    #                             'css/*.css',
    #                             'css/**/*.css',
    #                             filters=['cssmin'], output=css_file),
    #                         )
    config.add_webasset('sa_css', css_bundle)


def add_js_assets(config):                                  # pragma: no cover
    settings = config.registry.settings
    if not settings.get('sacrud.debug_js', False):
        return
    js_folder = os.path.join(settings["webassets.base_dir"], 'js')

    bower = ["jquery/dist/jquery.min.js",
             "chosen/public/chosen.jquery.min.js",
             "jquery-ui/ui/minified/jquery-ui.min.js",
             "speakingurl/speakingurl.min.js",
             "jqueryui-timepicker-addon/src/jquery-ui-timepicker-addon.js",
             "requirejs/require.js",
             "elfinder/src/elfinder/js/elfinder.js",
             "jquery-maskedinput/dist/jquery.maskedinput.min.js",
             "modernizr/modernizr.js",
             "pickadate/lib/compressed/picker.js",
             "pickadate/lib/compressed/picker.date.js",
             "pickadate/lib/compressed/picker.time.js",
             ]
    for f in bower:
        src = os.path.join(js_folder, 'bower_components', f)
        dst = os.path.join(js_folder, 'lib', f.split('/')[-1])
        copyfile(src, dst)


def includeme(config):
    config.include(webassets_init)
    config.include(add_css_assets)
    config.include(add_js_assets)
