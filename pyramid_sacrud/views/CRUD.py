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
import logging

import deform
import peppercorn
import transaction
from paginate_sqlalchemy import SqlalchemyOrmPage
from pyramid.compat import escape
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from sacrud.common import get_obj, pk_list_to_dict, pk_to_list
from sacrud_deform import SacrudForm
from sqlalchemy.orm.exc import NoResultFound

from . import (CREATE_TEMPLATE, LIST_TEMPLATE, SACRUD_EDIT_TEMPLATE,
               SACRUD_LIST_TEMPLATE, UPDATE_TEMPLATE)
from ..breadcrumbs import breadcrumbs
from ..common import (get_table, get_table_verbose_name, preprocessing_value,
                      sacrud_env)
from ..common.paginator import get_paginator
from ..exceptions import SacrudMessagedException
from ..includes.localization import _ps
from ..security import (PYRAMID_SACRUD_CREATE, PYRAMID_SACRUD_DELETE,
                        PYRAMID_SACRUD_LIST, PYRAMID_SACRUD_UPDATE)


class CRUD(object):

    def __init__(self, request):
        self.pk = None
        self.request = request
        self.tname = request.matchdict['table']
        self.table = get_table(self.tname, self.request)
        self.crud = self.request.dbsession.sacrud(self.table, commit=False)
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

    def get_response(self, options, template_attr):
        if hasattr(self.table, template_attr):
            return render_to_response(
                getattr(self.table, template_attr),
                sacrud_env(lambda x: options)(self),
                self.request)
        return options


class Add(CRUD):

    @sacrud_env
    @view_config(
        renderer=UPDATE_TEMPLATE,
        route_name=PYRAMID_SACRUD_UPDATE,
        permission=PYRAMID_SACRUD_UPDATE)
    @view_config(
        renderer=CREATE_TEMPLATE,
        route_name=PYRAMID_SACRUD_CREATE,
        permission=PYRAMID_SACRUD_CREATE)
    def sa_add(self):
        action = self.request.matched_route.name
        bc = breadcrumbs(self.tname, get_table_verbose_name(self.table),
                         action, self.pk)
        dbsession = self.request.dbsession
        try:
            obj = get_obj(dbsession, self.table, self.pk)
        except (NoResultFound, KeyError):
            raise HTTPNotFound
        form = SacrudForm(obj=obj, dbsession=dbsession,
                          request=self.request, table=self.table)()

        def options_for_response(form):
            return dict(form=form.render(),
                        pk=self.pk,
                        obj=obj,
                        breadcrumbs=bc,
                        pk_to_list=pk_to_list)

        if 'form.submitted' in self.request.params:
            controls = self.request.POST.items()
            pstruct = peppercorn.parse(controls)
            if '__formid__' in pstruct:
                try:
                    deserialized = form.validate_pstruct(pstruct).values()
                except deform.ValidationFailure as e:
                    return options_for_response(e)
                data = {k: preprocessing_value(v)
                        for d in deserialized
                        for k, v in d.items()}
            else:
                # if not peppercon format
                data = pstruct

            try:
                if action == PYRAMID_SACRUD_UPDATE:
                    obj = self.crud.update(self.pk, data)
                    flash_action = 'updated'
                else:
                    obj = self.crud.create(data)
                    flash_action = 'created'
                name = obj.__repr__()
                dbsession.flush()
            except SacrudMessagedException as e:
                self.flash_message(e.message, status=e.status)
                return self.get_response(options_for_response(form),
                                         SACRUD_EDIT_TEMPLATE)
            except Exception as e:
                transaction.abort()
                logging.exception("Something awful happened!")
                raise e
            transaction.commit()
            self.flash_message(_ps(
                u"You ${action} object of ${name}",
                mapping={'action': flash_action, 'name': escape(name or '')}
            ))
            return HTTPFound(
                location=self.request.route_url(PYRAMID_SACRUD_LIST,
                                                table=self.tname))
        return self.get_response(options_for_response(form),
                                 SACRUD_EDIT_TEMPLATE)


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
                    obj = self.crud.delete(pk)
                    obj_list.append(obj['name'])
                except (NoResultFound, KeyError):
                    raise HTTPNotFound
                except SacrudMessagedException as e:
                    self.flash_message(e.message, status=e.status)
                except Exception as e:
                    transaction.abort()
                    logging.exception("Something awful happened!")
                    raise e
            transaction.commit()
            self.flash_message(_ps("You delete the following objects:"))
            self.flash_message("<br/>".join(
                [escape(x or '') for x in obj_list]))
            return HTTPFound(
                location=self.request.route_url(PYRAMID_SACRUD_LIST,
                                                table=self.tname))

    @sacrud_env
    @view_config(
        renderer=LIST_TEMPLATE,
        route_name=PYRAMID_SACRUD_LIST,
        permission=PYRAMID_SACRUD_LIST)
    def sa_list(self):
        delete_action = self.make_selected_action()
        if delete_action:
            return delete_action
        items_per_page = getattr(self.table, 'items_per_page', 10)
        rows = self.crud.read()
        try:
            paginator_attr = get_paginator(self.request, items_per_page - 1)
        except ValueError:
            raise HTTPNotFound
        paginator = SqlalchemyOrmPage(rows, **paginator_attr)
        options = {'rows': rows,
                   'paginator': paginator,
                   'pk_to_list': pk_to_list,
                   'breadcrumbs': breadcrumbs(
                       self.tname,
                       get_table_verbose_name(self.table),
                       PYRAMID_SACRUD_LIST)}
        return self.get_response(options, SACRUD_LIST_TEMPLATE)


class Delete(CRUD):

    @view_config(
        route_name=PYRAMID_SACRUD_DELETE,
        permission=PYRAMID_SACRUD_DELETE)
    def sa_delete(self):
        try:
            obj = self.crud.delete(self.pk)
            transaction.commit()
        except (NoResultFound, KeyError):
            raise HTTPNotFound
        self.flash_message(_ps("You have removed object of ${name}",
                               mapping={'name': escape(obj['name'] or '')}))
        return HTTPFound(
            location=self.request.route_url(PYRAMID_SACRUD_LIST,
                                            table=self.tname))
