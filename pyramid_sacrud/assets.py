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


def add_js_assets(config):                                  # pragma: no cover
    settings = config.registry.settings
    if not settings.get('sacrud.debug_js', False):
        return
    here = os.path.dirname(__file__)
    js_folder = os.path.join(here, 'static', 'js')

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
    config.include(add_js_assets)
