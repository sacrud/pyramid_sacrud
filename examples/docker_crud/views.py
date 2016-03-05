#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

from pyramid.view import view_config
from pyramid.traversal import resource_path
from pyramid.httpexceptions import HTTPFound

import docker
from paginate import Page
from resources import Image, UpdateFactory, MassAction
from pyramid_sacrud import PYRAMID_SACRUD_VIEW


@view_config(
    context=Image,
    renderer='ps_crud/list.jinja2',
    route_name=PYRAMID_SACRUD_VIEW
)
def admin_docker_list_view(context, request):
    """Show list of docker images."""
    return {
        'paginator': Page(
            context.all,
            url_maker=lambda p: request.path_url + "?page=%s" % p,
            page=int(request.params.get('page', 1)),
            items_per_page=6
        )
    }


@view_config(
    context=MassAction,
    request_param='mass_action=delete',
    route_name=PYRAMID_SACRUD_VIEW
)
def admin_docker_massaction_view(context, request):
    """Mass action view."""
    items_list = request.POST.getall('selected_item')
    for item in items_list:
        try:
            context.cli.remove_image(item)
            request.session.flash(["deleted {}".format(item), "success"])
        except docker.errors.APIError as e:
            request.session.flash([e.explanation, "error"])
    url = "/" + request.sacrud_prefix + "/" + resource_path(context.__parent__)
    return HTTPFound(location=url)


@view_config(
    context=UpdateFactory.Update,
    renderer='target.jinja2',
    route_name=PYRAMID_SACRUD_VIEW
)
def admin_docker_update_view(context, request):
    from pprint import pformat
    return {'data': '<pre>' + pformat(context.img) + '</pre>'}
