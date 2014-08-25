#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
import os
from deform.widget import TextInputWidget, TextAreaWidget

cur_path = os.path.dirname(os.path.realpath(__file__))
deform_path = os.path.join(cur_path, '..', 'templates', 'deform')


class ElfinderWidget(TextInputWidget):
    template = os.path.join(deform_path, 'Elfinder.pt')


class HstoreWidget(TextAreaWidget):
    template = os.path.join(deform_path, 'Hstore.pt')


class SlugWidget(TextInputWidget):
    template = os.path.join(deform_path, 'Slug.pt')
