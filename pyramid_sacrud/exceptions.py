#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Exceptions for pyramid_sacrud
"""


class SacrudMessagedException(Exception):
    """ Just raise this exception

    .. code-block:: python

        raise SacrudMessagedException('My Super Message', status='error')

    status = error|warning|success
    """

    def __init__(self, message, status='error'):
        self.status = status
        self.message = message

    def __str__(self):
        return repr(self.message)
