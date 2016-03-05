#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Resources fro Docker
"""
import time

from zope.interface import implementer

import docker
from pyramid_sacrud.interfaces import ISacrudResource


@implementer(ISacrudResource)
class Docker(object):

    breadcrumb = True

    def __init__(self):
        self.cli = docker.Client(base_url='unix://var/run/docker.sock')

    @property
    def verbose_name(self):
        return self.__class__.__name__ + "'s"

    @property
    def __name__(self):
        return self.verbose_name


class Image(Docker):

    def _get_id(self, row):
        return row['Id']

    @property
    def _columns(self):
        class Column:
            def __init__(self, name, value):
                self.name = name
                self.value = value

            def value(self, row):
                return self.value(row)
        return (
            Column("id", lambda x: x["Id"][:10]),
            Column("created",
                   lambda x: time.strftime("%D %H:%M",
                                           time.localtime(
                                               int(x["Created"])
                                           ))),
            Column("tag", lambda x: x["RepoTags"][0])
        )

    def __getitem__(self, name):

        if name == 'mass_action':
            return self.ps_crud["crud"]["mass_action"]
        elif name == 'update':
            return self.ps_crud["crud"]["update"]

    @property
    def ps_crud(self):
        mass_action = MassAction()
        mass_action.__parent__ = self
        update = UpdateFactory()
        update.__parent__ = self
        return {
            "get_id": self._get_id,
            "columns": self._columns,
            "crud": {
                "mass_action": mass_action,
                "update": update,
            }
        }

    @property
    def all(self):
        return self.cli.images()


class UpdateFactory(object):

    __name__ = "update"

    def __getitem__(self, name):
        return self.Update(name, self)

    def __call__(self, row):
        return self[row["Id"]]

    class Update(Docker):

        __name__ = None

        def get_image(self, img_id):
            for img in self.cli.images():
                if img['Id'] == img_id:
                    return img

        def __init__(self, name, parent):
            Docker.__init__(self)
            self.__name__ = name
            self.__parent__ = parent
            self.img = self.get_image(name)
            self.ps_crud = parent.__parent__.ps_crud


class MassAction(Docker):

    __name__ = 'mass_action'
