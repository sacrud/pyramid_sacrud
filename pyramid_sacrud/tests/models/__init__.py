#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
SQLAlchemy settings
"""
import os

from pyramid.threadlocal import get_current_request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from sacrud import CRUDSession

Base = declarative_base()

DIRNAME = os.path.dirname(__file__)
DATABASE_FILE = os.path.join(DIRNAME, 'test.sqlite')
TEST_DATABASE_CONNECTION_STRING = 'sqlite:///%s' % DATABASE_FILE
engine = create_engine(TEST_DATABASE_CONNECTION_STRING)
Session = scoped_session(sessionmaker(bind=engine, class_=CRUDSession),
                         scopefunc=get_current_request)
