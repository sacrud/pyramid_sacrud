#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Webhelpers paginator
"""
from webhelpers.paginate import PageURL_WebOb


def get_current_page(request):
    return int(request.params.get('page', 1))


def get_paginator(request, items_per_page=10):
    page_url = PageURL_WebOb(request)
    paginator = {"url": page_url, "items_per_page": items_per_page,
                 "page": get_current_page(request)}
    return paginator
