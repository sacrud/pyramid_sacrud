#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Resources of pyramid_sacrud
"""


class GroupResource(object):

    def __init__(self, group, resources):
        self.group = group
        self.resources = resources

    def __getitem__(self, name):
        for resource in self.resources:
            if resource.__name__ == name:
                resource.parent = self
                return resource

    @property
    def __name__(self):
        return str(self.group)
