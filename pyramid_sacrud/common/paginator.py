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
from paginate import Page, make_html_tag


def paginate_link_tag(item):
    """
    Create an A-HREF tag that points to another page usable in paginate.
    """
    a_tag = Page.default_link_tag(item)
    if item['type'] == 'current_page':
        return make_html_tag('li', a_tag, **{'class': 'blue white-text'})
    return make_html_tag('li', a_tag)


def get_current_page(request):
    return int(request.params.get('page', 1))


def get_paginator(request, items_per_page=10):
    return {
        "items_per_page": items_per_page,
        "page": get_current_page(request),
        "url_maker": lambda p: request.path_url + "?page=%s" % p,
        "link_tag": paginate_link_tag
    }
