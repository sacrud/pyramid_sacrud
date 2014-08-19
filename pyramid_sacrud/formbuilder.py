#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
import colander
import deform
from deform import Form
from sqlalchemy import types as sa_types

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
    def __init__(self, group, columns, table, **kwargs):
        kwargs['title'] = group
        colander.SchemaNode.__init__(self, colander.Mapping('ignore'), **kwargs)
        self.table = table
        self.add_colums(columns)

    def get_column_name(self, col):
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

    def add_colums(self, columns):
        for col in columns:
            if isinstance(col, dict):
                col = Dict2Obj(col)
            name = self.get_column_name(col)
            description = self.get_column_description(col)
            sa_type = self.get_column_type(col)
            column_type = _get_column_type_by_sa_type(sa_type)
            widget_type = _get_widget_type_by_sa_type(sa_type)
            css_class = self.get_column_css_styles(self.table, col)
            node = colander.SchemaNode(column_type(),
                                       name=name,
                                       description=description,
                                       widget=widget_type(css_class=css_class)
                                       )
            self.add(node)


class SacrudShemaNode(colander.SchemaNode):
    def __init__(self, **kwargs):
        colander.SchemaNode.__init__(self, colander.Mapping('ignore'), **kwargs)
        self.obj = kwargs['obj']
        self.obj_cls = kwargs['table']
        self.visible_columns = kwargs['col']
        self.build()

    def build(self):
        for group, columns in self.visible_columns:
            self.add(GroupShema(group, columns, self.obj_cls))


def form_generator(**kwargs):
    schema = SacrudShemaNode(**kwargs)
    submit = deform.Button(name='form.submitted', title="save",
                           css_class='toolbar-button__item')
    return Form(schema, buttons=(submit,))
