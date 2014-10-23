#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Applications for project
"""


def includeme(config):
    config.include('.assets')
    config.include('.routes')
    config.include('.database')
    config.include('.localization')
