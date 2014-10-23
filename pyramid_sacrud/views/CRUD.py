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

import deform
from paginate_sqlalchemy import SqlalchemyOrmPage
from peppercorn import parse
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config

from pyramid_sacrud.breadcrumbs import breadcrumbs
from pyramid_sacrud.common import get_settings_param, sacrud_env
from pyramid_sacrud.common.paginator import get_paginator
from sacrud import action
from sacrud.common import columns_by_group, get_obj, pk_to_list
from sacrud_deform import form_generator

from ..security import (PYRAMID_SACRUD_CREATE, PYRAMID_SACRUD_DELETE,
                        PYRAMID_SACRUD_LIST, PYRAMID_SACRUD_UPDATE)


def get_table(tname, request):
    """ Return table by table name from pyramid_sacrud.models in settings.
    """
    # convert values of models dict to flat list
    setting_params = get_settings_param(request, 'pyramid_sacrud.models').values()
    tables_lists = [x['tables'] for x in setting_params]
    tables = itertools.chain(*tables_lists)
    tables = [table for table in tables if (table.__tablename__).
              lower() == tname.lower()]
    if not tables:
        return None
    return tables[0]


def get_table_verbose_name(table):
    if hasattr(table, 'verbose_name'):
        return table.verbose_name
    elif hasattr(table, '__tablename__'):
        return table.__tablename__
    return table.name


def update_difference_object(obj, key, value):
    if isinstance(obj, dict):
        obj.update({key: value})
    else:
        setattr(obj, key, value)


def pk_list_to_dict(pk_list):
    if pk_list and len(pk_list) % 2 == 0:
        return dict(zip(pk_list[::2], pk_list[1::2]))
    return None


def request_to_sacrud(r):
    fields = r.POST.items()
    data = parse(fields)

    _r = {}

    def request_to_flat(request):
        for key, value in request.items():
            if type(value) is dict:
                if 'upload' in value:
                    upload = value['upload']
                    if hasattr(upload, 'file'):
                        if upload.file:
                            _r[key] = upload
                else:
                    request_to_flat(value)
                continue
            _r[key] = value

    request_to_flat(data)
    return _r


class CRUD(object):

    def __init__(self, request):
        self.pk = None
        self.request = request
        self.tname = request.matchdict['table']
        self.table = get_table(self.tname, self.request)
        self.params = request.params
        if hasattr(self.params, 'dict_of_lists'):
            self.params = self.params.dict_of_lists()

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

    @sacrud_env
    @view_config(route_name='sa_list', renderer='/sacrud/list.jinja2',
                 permission=PYRAMID_SACRUD_LIST)
    def sa_list(self):
        table = self.table
        request = self.request

        # Some actions with objects in grid
        selected_action = request.POST.get('selected_action')
        items_list = request.POST.getall('selected_item')
        if selected_action == 'delete':
            for item in items_list:
                pk_list = json.loads(item)
                pk = pk_list_to_dict(pk_list)
                action.CRUD(request.dbsession, table, pk=pk).delete()

        # paginator
        items_per_page = getattr(table, 'items_per_page', 10)

        resp = action.CRUD(request.dbsession, table).rows_list()
        paginator_attr = get_paginator(request, items_per_page)
        paginator = SqlalchemyOrmPage(resp['row'], **paginator_attr)

        return {'sa_crud': resp,
                'paginator': paginator,
                'pk_to_list': pk_to_list,
                'breadcrumbs': breadcrumbs(self.tname,
                                           get_table_verbose_name(self.table),
                                           'sa_list')}

    @sacrud_env
    @view_config(route_name='sa_update', renderer='/sacrud/create.jinja2',
                 permission=PYRAMID_SACRUD_UPDATE)
    @view_config(route_name='sa_create', renderer='/sacrud/create.jinja2',
                 permission=PYRAMID_SACRUD_CREATE)
    def sa_add(self):
        bc = breadcrumbs(self.tname,
                         get_table_verbose_name(self.table), 'sa_create')
        if self.pk:
            bc = breadcrumbs(self.tname,
                             get_table_verbose_name(self.table),
                             'sa_update', id=self.pk)
        dbsession = self.request.dbsession
        obj = get_obj(dbsession, self.table, self.pk)
        columns = columns_by_group(self.table)

        form, js_list = form_generator(dbsession=dbsession,
                                       obj=obj,
                                       table=self.table,
                                       columns_by_group=columns,
                                       request=self.request)
        resp = action.CRUD(self.request.dbsession, self.table, self.pk)

        if 'form.submitted' in self.request.params:
            controls = self.request.POST.items()
            try:
                form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                sa_crud = {'obj': obj,
                           'pk': self.pk,
                           'col': columns,
                           'table': self.table
                           }
                return dict(form=e.render(),
                            sa_crud=sa_crud,
                            js_list=js_list,
                            breadcrumbs=bc,
                            pk_to_list=pk_to_list)
            resp.request = request_to_sacrud(self.request)
            resp.add()
            if self.pk:
                self.flash_message("You updated object of %s" % self.tname)
            else:
                self.flash_message("You created new object of %s" % self.tname)
            return HTTPFound(location=self.request.route_url('sa_list',
                                                             table=self.tname))
        sa_crud = resp.add()
        return {'form': form.render(),
                'sa_crud': sa_crud,
                'pk_to_list': pk_to_list,
                'js_list': js_list,
                'breadcrumbs': bc}

    @view_config(route_name='sa_delete', permission=PYRAMID_SACRUD_DELETE)
    def sa_delete(self):
        action.CRUD(self.request.dbsession, self.table, pk=self.pk).delete()
        self.flash_message("You have removed object of %s" % self.tname)
        return HTTPFound(location=self.request.route_url('sa_list',
                                                         table=self.tname))
