#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Views for Pyramid frontend
"""
import itertools
import json

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import inspect

from pyramid_sacrud.breadcrumbs import breadcrumbs
from pyramid_sacrud.common import get_settings_param, sacrud_env
from sacrud import action
from sacrud.common.paginator import get_paginator
from sacrud.common.sa_helpers import pk_to_list


def get_table(tname, request):
    """ Return table by table name from pyramid_sacrud.models in settings.
    """
    # convert values of models dict to flat list
    setting_params = get_settings_param(request, 'pyramid_sacrud.models').values()
    tables_lists = map(lambda x: x['tables'], setting_params)
    tables = itertools.chain(*tables_lists)
    tables = filter(lambda table: (table.__tablename__).
                    lower() == tname.lower(), tables)
    if not tables:
        return None
    return tables[0]


def get_relationship(tname, request):
    table = get_table(tname, request)
    if not table:
        return None
    relations = inspect(table).relationships
    return [rel for rel in relations]


def update_difference_object(obj, key, value):
    if isinstance(obj, dict):
        obj.update({key: value})
    else:
        setattr(obj, key, value)
    # return obj


def pk_list_to_dict(pk_list):
    if pk_list and len(pk_list) % 2 == 0:
        return dict(zip(pk_list[::2], pk_list[1::2]))
    return None


class CRUD(object):

    def __init__(self, request):
        self.pk = None
        self.request = request
        self.tname = request.matchdict['table']
        self.table = get_table(self.tname, self.request)
        self.relationships = get_relationship(self.tname, self.request)
        self.params = request.params.dict_of_lists()

        if not self.table:
            raise HTTPNotFound

        pk = request.matchdict.get('pk')
        if pk and len(pk) % 2 == 0:
            self.pk = pk_list_to_dict(pk)
        elif pk or pk == ():
            raise HTTPNotFound

    def flash_message(self, message, status="success"):
        if hasattr(self.request, 'session'):
            self.request.session.flash([message, status])

    # XXX: C901
    @sacrud_env
    @view_config(route_name='sa_list', renderer='/sacrud/list.jinja2')
    def sa_list(self):
        table = self.table
        request = self.request
        order_by = request.params.get('order_by', False)
        search = request.params.get('search')
        get_params = {'order_by': order_by, 'search': search}

        # Make url for table headrow links to order_by
        for col in getattr(table, 'sacrud_list_col', table.__table__.columns):
            order_param_list = []
            column_name = col['column'].name if isinstance(col, dict) else col.name
            if order_by:
                if column_name not in order_by.replace('-', '').split('.'):
                    order_param_list.append(column_name)

                for value in order_by.split('.'):
                    none, pfx, col_name = value.rpartition('-')
                    if column_name == col_name:
                        new_pfx = {'': '-', '-': ''}[pfx]
                        order_param_list.insert(0, '%s%s' % (new_pfx, col_name))
                    else:
                        order_param_list.append('%s%s' % (pfx, col_name))
            else:
                order_param_list.append(column_name)

            full_params = ['%s=%s' % (param, value) for param, value in get_params.items()
                           if param != 'order_by' and value]
            full_params.append('order_by=%s' % '.'.join(order_param_list))
            update_difference_object(col, 'head_url', '&'.join(full_params))

        # Some actions with objects in grid
        selected_action = request.POST.get('selected_action')
        items_list = request.POST.getall('selected_item')
        if selected_action == 'delete':
            for item in items_list:
                pk_list = json.loads(item)
                pk = pk_list_to_dict(pk_list)
                action.CRUD(request.dbsession, table, pk=pk).delete()

        items_per_page = getattr(table, 'items_per_page', 10)
        resp = action.CRUD(request.dbsession, table)\
            .rows_list(paginator=get_paginator(request, items_per_page),
                       order_by=order_by, search=search)

        return {'sa_crud': resp,
                'pk_to_list': pk_to_list,
                'breadcrumbs': breadcrumbs(self.tname, 'sa_list'),
                'get_params': get_params}

    @sacrud_env
    @view_config(route_name='sa_update', renderer='/sacrud/create.jinja2')
    @view_config(route_name='sa_create', renderer='/sacrud/create.jinja2')
    def sa_add(self):
        resp = action.CRUD(self.request.dbsession, self.table, self.pk)

        if 'form.submitted' in self.request.params:
            resp.request = self.params
            resp.add()
            if self.pk:
                self.flash_message("You updated object of %s" % self.tname)
            else:
                self.flash_message("You created new object of %s" % self.tname)
            return HTTPFound(location=self.request.route_url('sa_list',
                                                             table=self.tname))

        bc = breadcrumbs(self.tname, 'sa_create')
        if self.pk:
            bc = breadcrumbs(self.tname, 'sa_update', id=self.pk)

        return {'sa_crud': resp.add(),
                'pk_to_list': pk_to_list,
                'relationships': self.relationships,
                'breadcrumbs': bc}

    @view_config(route_name='sa_delete')
    def sa_delete(self):
        action.CRUD(self.request.dbsession, self.table, pk=self.pk).delete()
        self.flash_message("You have removed object of %s" % self.tname)
        return HTTPFound(location=self.request.route_url('sa_list',
                                                         table=self.tname))
