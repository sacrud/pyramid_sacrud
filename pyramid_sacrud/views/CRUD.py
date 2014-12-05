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
import json

import deform
import transaction
from paginate_sqlalchemy import SqlalchemyOrmPage
from pyramid.compat import escape
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound

from sacrud import action
from sacrud.common import (columns_by_group, get_flat_columns, get_obj,
                           pk_list_to_dict, pk_to_list)
from sacrud_deform import form_generator

from ..breadcrumbs import breadcrumbs
from ..common import (get_table, get_table_verbose_name, request_to_sacrud,
                      sacrud_env)
from ..common.custom import Widget
from ..common.paginator import get_paginator
from ..exceptions import SacrudMessagedException
from ..includes.localization import _ps
from ..security import (PYRAMID_SACRUD_CREATE, PYRAMID_SACRUD_DELETE,
                        PYRAMID_SACRUD_LIST, PYRAMID_SACRUD_UPDATE)


class EventsCRUD(object):

    def event_add(self, obj, values):
        self.widget_postprocessing(obj, values)

    def widget_postprocessing(self, obj, values):
        columns = get_flat_columns(self.table)
        session = self.request.dbsession
        for column in columns:
            if not isinstance(column, Widget):
                continue
            column.postprocessing(obj, session, values)


class BaseCRUD(object):

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


class CRUD(BaseCRUD, EventsCRUD):
    pass


class Add(CRUD):

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
        try:
            obj = get_obj(dbsession, self.table, self.pk)
        except (NoResultFound, KeyError):
            raise HTTPNotFound
        columns = columns_by_group(self.table)
        form, js_list = form_generator(dbsession=dbsession,
                                       obj=obj,
                                       table=self.table,
                                       columns_by_group=columns,
                                       request=self.request)
        resp = action.CRUD(self.request.dbsession, self.table, self.pk)

        def get_responce(form, sa_crud=None):
            if not sa_crud:
                sa_crud = {'obj': obj,
                           'pk': self.pk,
                           'col': columns,
                           'table': self.table
                           }
            return dict(form=form.render(),
                        sa_crud=sa_crud,
                        js_list=js_list,
                        breadcrumbs=bc,
                        pk_to_list=pk_to_list)

        if 'form.submitted' in self.request.params:
            controls = self.request.POST.items()
            try:
                form.validate(controls)
            except deform.ValidationFailure as e:
                return get_responce(e)
            values = request_to_sacrud(self.request)
            resp.request = values
            try:
                obj_as_dict = resp.add(commit=False)
                obj = obj_as_dict['obj']
                self.event_add(obj, values)
                dbsession.flush()
            except SacrudMessagedException as e:
                self.flash_message(e.message, status=e.status)
                return get_responce(form)
            except Exception as e:
                transaction.abort()
                raise e
            transaction.commit()
            if self.pk:
                self.flash_message(
                    _ps(u"You updated object of ${name}",
                        mapping={'name': escape(obj_as_dict['name'])}))
            else:
                self.flash_message(
                    _ps("You created new object of ${name}",
                        mapping={'name': escape(obj_as_dict['name'])}))
            return HTTPFound(location=self.request.route_url('sa_list',
                                                             table=self.tname))
        sa_crud = resp.add()
        return get_responce(form, sa_crud)


class List(CRUD):

    def make_selected_action(self):
        selected_action = self.request.POST.get('selected_action')
        items_list = None
        try:
            items_list = self.request.POST.getall('selected_item')
        except AttributeError:
            items_list = self.request.POST.get('selected_item')
        if selected_action == 'delete':
            obj_list = []
            for item in items_list:
                pk_list = json.loads(item)
                pk = pk_list_to_dict(pk_list)
                try:
                    obj = action.CRUD(self.request.dbsession,
                                      self.table, pk=pk).delete(commit=False)
                    obj_list.append(obj['name'])
                except NoResultFound:
                    raise HTTPNotFound
            self.flash_message(_ps("You delete the following objects:"))
            self.flash_message("<br/>".join(map(escape, obj_list)))

    @sacrud_env
    @view_config(route_name='sa_list', renderer='/sacrud/list.jinja2',
                 permission=PYRAMID_SACRUD_LIST)
    def sa_list(self):
        self.make_selected_action()
        items_per_page = getattr(self.table, 'items_per_page', 10)
        resp = action.CRUD(self.request.dbsession, self.table).rows_list()
        try:
            paginator_attr = get_paginator(self.request, items_per_page - 1)
        except ValueError:
            raise HTTPNotFound
        paginator = SqlalchemyOrmPage(resp['row'], **paginator_attr)
        return {'sa_crud': resp,
                'paginator': paginator,
                'pk_to_list': pk_to_list,
                'breadcrumbs': breadcrumbs(self.tname,
                                           get_table_verbose_name(self.table),
                                           'sa_list')}


class Delete(CRUD):

    @view_config(route_name='sa_delete', permission=PYRAMID_SACRUD_DELETE)
    def sa_delete(self):
        try:
            obj = action.CRUD(self.request.dbsession,
                              self.table, pk=self.pk).delete()
        except (NoResultFound, KeyError):
            raise HTTPNotFound
        self.flash_message(_ps("You have removed object of ${name}",
                               mapping={'name': escape(obj['name'])}))
        return HTTPFound(location=self.request.route_url('sa_list',
                                                         table=self.tname))
