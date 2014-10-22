#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Custom gettext for pyramid_sacrud
"""
from pyramid.events import BeforeRender, NewRequest, subscriber
from pyramid.i18n import get_localizer

from ..localization import _ps


@subscriber(BeforeRender)
def add_renderer_globals(event):
    request = event['request']
    event['_ps'] = request.translate


@subscriber(NewRequest)
def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)

    def auto_translate(string):
        return localizer.translate(_ps(string))
    request.localizer = localizer
    request.translate = auto_translate
