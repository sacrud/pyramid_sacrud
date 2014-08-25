#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
import colander
import deform
import sqlalchemy
from deform import Form
from sqlalchemy import types as sa_types
from sqlalchemy.dialects.postgresql import JSON, HSTORE
from .widgets import ElfinderWidget, HstoreWidget, SlugWidget

import sacrud

# Map sqlalchemy types to colander types.
_TYPES = {
    sa_types.BigInteger: colander.Integer,
    sa_types.Boolean: colander.Boolean,
    sa_types.Date: colander.Date,
    sa_types.DateTime: colander.DateTime,
    sa_types.Enum: colander.String,
    sa_types.Float: colander.Float,
    sa_types.Integer: colander.Integer,
    sa_types.Numeric: colander.Decimal,
    sa_types.SmallInteger: colander.Integer,
    sa_types.String: colander.String,
    sa_types.Text: colander.String,
    sa_types.Time: colander.Time,
    sa_types.Unicode: colander.String,
    sa_types.UnicodeText: colander.String,
    JSON: colander.String,
    HSTORE: colander.String,
    sqlalchemy.ForeignKey: colander.String,
    sacrud.exttype.ChoiceType: colander.String,
    sacrud.exttype.FileStore: deform.FileData,
    sacrud.exttype.SlugType: colander.String,
}

# Map sqlalchemy types to deform widgets.
_WIDGETS = {
    sa_types.BigInteger: deform.widget.TextInputWidget,
    sa_types.Boolean: deform.widget.CheckboxWidget,
    sa_types.Date: deform.widget.DateInputWidget,
    sa_types.DateTime: deform.widget.DateTimeInputWidget,
    sa_types.Enum: deform.widget.SelectWidget,
    sa_types.Float: deform.widget.TextInputWidget,
    sa_types.Integer: deform.widget.TextInputWidget,
    sa_types.Numeric: deform.widget.TextInputWidget,
    sa_types.SmallInteger: deform.widget.TextInputWidget,
    sa_types.String: deform.widget.TextInputWidget,
    sa_types.Text: deform.widget.TextAreaWidget,
    sa_types.Time: deform.widget.TextInputWidget,
    sa_types.Unicode: deform.widget.TextInputWidget,
    sa_types.UnicodeText: deform.widget.TextAreaWidget,
    JSON: deform.widget.TextAreaWidget,
    HSTORE: HstoreWidget,
    sqlalchemy.ForeignKey: deform.widget.SelectWidget,
    sacrud.exttype.ChoiceType: deform.widget.SelectWidget,
    sacrud.exttype.FileStore: deform.widget.FileUploadWidget,
    sacrud.exttype.ElfinderString: ElfinderWidget,
    sacrud.exttype.SlugType: SlugWidget,
}


class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        """"""
        attrs = str([x for x in self.__dict__])
        return "<Dict2Obj: %s>" % attrs


def _get_column_type_by_sa_type(sa_type):
    """
    Returns the colander type that correspondents to the sqlalchemy type
    'sa_type'.
    """
    return _TYPES.get(sa_type) or colander.String


def _get_widget_type_by_sa_type(sa_type):
    """
    Returns the deform widget that correspondents to the sqlalchemy type
    'sa_type'.
    """
    return _WIDGETS.get(sa_type) or deform.widget.TextInputWidget


class HTMLText(object):
    def __init__(self, text):
        self.text = text

    def __html__(self):
        return unicode(self.text)


class GroupShema(colander.Schema):
    def __init__(self, relationships, group, columns, table, obj, dbsession,
                 **kwargs):
        kwargs['title'] = group
        colander.SchemaNode.__init__(self, colander.Mapping('ignore'), **kwargs)
        self.obj = obj
        self.table = table
        self.relationships = relationships
        self.dbsession = dbsession
        self.js_list = []

        self.add_colums(columns)

    def get_column_title(self, col):
        if 'verbose_name' in col.info:
            name = col.info['verbose_name']
        else:
            name = col.name
        if 'sacrud_position' in col.info:
            if col.info['sacrud_position'] == 'inline':
                if 'verbose_name' in col.info:
                    name = col.info['verbose_name']
                else:
                    name = col.sacrud_name
        return name

    def get_column_description(self, col):
        if 'description' in col.info:
            return HTMLText(col.info['description'])
        return None

    def get_column_css_styles(self, table, col):
        css_class = []
        if hasattr(table, 'sacrud_css_class'):
            for key, value in table.sacrud_css_class.items():
                if col in value:
                    css_class.append(key)
            return ' '.join(css_class)
        return None

    def get_column_type(self, col):
        if hasattr(col, 'type'):
            return col.type.__class__
        return None

    def get_col_default_value(self, col, obj):
        value = None
        col_type = self.get_column_type(col)
        if obj and hasattr(col, 'instance_name'):
            value = obj.__getattribute__(col.instance_name)
        elif obj and hasattr(col, 'name'):
            value = obj.__getattribute__(col.name)
        if value is None:
            value = colander.null
        elif col_type == sacrud.exttype.ChoiceType:
            value = value[0]
        return value

    def get_widget(self, widget_type, values, mask, css_class,
                   col):
        if widget_type == deform.widget.FileUploadWidget:
            return widget_type(None)
        return widget_type(values=values,
                           mask=mask,
                           col=col,
                           mask_placeholder='_',
                           css_class=css_class)

    def get_node(self, values=None, mask=None, **kwargs):
        column_type = _get_column_type_by_sa_type(kwargs['sa_type'])
        widget_type = _get_widget_type_by_sa_type(kwargs['sa_type'])
        if kwargs['sa_type'] == sa_types.Enum and not values:
            values = [(x, x) for x in kwargs['col'].type.enums]
        if kwargs['sa_type'] == sacrud.exttype.GUID and not mask:
            mask = 'hhhhhhhh-hhhh-hhhh-hhhh-hhhhhhhhhhhh'
        if kwargs['sa_type'] == sacrud.exttype.ChoiceType and not values:
            values = [(v, k) for k, v in kwargs['col'].type.choices.items()]
        if kwargs['sa_type'] == sacrud.exttype.ElfinderString:
            self.js_list.append('elfinder.js')
        if kwargs['sa_type'] == sacrud.exttype.SlugType:
            self.js_list.append('speakingurl.min.js')
        widget = self.get_widget(widget_type, values, mask,
                                 kwargs['css_class'],
                                 kwargs['col'])
        if widget_type == deform.widget.FileUploadWidget:
            kwargs['description'] = kwargs['default']
            kwargs['default'] = colander.null
        node = colander.SchemaNode(column_type(),
                                   title=kwargs['title'],
                                   name=kwargs['col'].name,
                                   default=kwargs['default'],
                                   description=kwargs['description'],
                                   widget=widget,
                                   )
        return node

    # TODO: rewrite it
    def get_foreign_key_node(self, **kwargs):
        from sacrud.common import pk_to_list
        fk_schema = colander.Schema()
        kwargs['sa_type'] = sqlalchemy.ForeignKey
        for rel in self.relationships:
            if kwargs['col'] in rel.remote_side or kwargs['col'] in rel.local_columns:
                choices = self.dbsession.query(rel.mapper).all()
                choices = [('', '')] + [(getattr(ch, pk_to_list(ch)[0]),
                                         ch.__repr__()) for ch in choices]
                node = self.get_node(values=choices, **kwargs)
                fk_schema.add(node)
                break
        return fk_schema

    def add_colums(self, columns):
        for col in columns:
            node = None
            if isinstance(col, dict):
                col = Dict2Obj(col)
            title = self.get_column_title(col)
            default = self.get_col_default_value(col, self.obj)
            description = self.get_column_description(col)
            css_class = self.get_column_css_styles(self.table, col)
            sa_type = self.get_column_type(col)
            params = {'col': col,
                      'sa_types': sa_type,
                      'title': title,
                      'description': description,
                      'default': default,
                      'css_class': css_class,
                      'sa_type': sa_type,
                      }
            if hasattr(col, 'foreign_keys'):
                if col.foreign_keys:
                    node = self.get_foreign_key_node(**params)
            if not node:
                node = self.get_node(**params)
            self.add(node)


class SacrudShemaNode(colander.SchemaNode):
    def __init__(self, relationships, dbsession, **kwargs):
        colander.SchemaNode.__init__(self, colander.Mapping('ignore'), **kwargs)
        self.obj = kwargs['obj']
        self.table = kwargs['table']
        self.visible_columns = kwargs['col']
        self.relationships = relationships
        self.dbsession = dbsession
        self.js_list = []

        self.build()

    def build(self):
        for group, columns in self.visible_columns:
            gs = GroupShema(self.relationships, group, columns,
                            self.table, self.obj, self.dbsession)
            self.add(gs)
            for lib in gs.js_list:
                self.js_list.append(lib)


def form_generator(relationships, dbsession, **kwargs):
    schema = SacrudShemaNode(relationships, dbsession, **kwargs)
    submit = deform.Button(name='form.submitted', title="save",
                           css_class='toolbar-button__item')
    return {'form': Form(schema, buttons=(submit,)),
            'js_list': schema.js_list,
            }
