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


class GroupShema(colander.Schema):
    def __init__(self, group, columns, **kwargs):
        kwargs['title'] = group
        colander.SchemaNode.__init__(self, colander.Mapping('ignore'), **kwargs)
        for col in columns:
            if isinstance(col, dict):
                col = Dict2Obj(col)
            if hasattr(col.info, 'verbose_name'):
                name = col.info['verbose_name']
            else:
                name = col.name
            if hasattr(col.info, 'sacrud_position'):
                if col.info['sacrud_position'] == 'inline':
                    name = col.info['verbose_name'] or col.sacrud_name
            node = colander.SchemaNode(colander.String(), name=name)
            self.add(node)


class SacrudShemaNode(colander.SchemaNode):
    def __init__(self, **kwargs):
        colander.SchemaNode.__init__(self, colander.Mapping('ignore'), **kwargs)
        self.obj = kwargs['obj']
        self.obj_cls = kwargs['table']
        self.visible_columns = kwargs['col']

        node = colander.SchemaNode(colander.String(), name="foo")
        self.add(node)
        for group, columns in self.visible_columns:
            self.add(GroupShema(group, columns))


def form_generator(**kwargs):
    schema = SacrudShemaNode(**kwargs)
    submit = deform.Button(name='form.submitted', title="save",
                           css_class='toolbar-button__item')
    myform = Form(schema, buttons=(submit,))
    return myform
