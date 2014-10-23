#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Internationalization and Localization
"""
from pyramid.i18n import TranslationStringFactory

_ps = TranslationStringFactory('pyramid_sacrud')


def includeme(config):
    config.add_translation_dirs('pyramid_sacrud:locale/')
    config.scan('.views')
