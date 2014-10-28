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
from pyramid.threadlocal import get_current_request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

TEST_DATABASE_CONNECTION_STRING = 'sqlite:///:memory:'

# an Engine, which the Session will use for connection
# resources
# engine = create_engine('sqlite:///pyramid_sacrud_tests.sqlite')
engine = create_engine(TEST_DATABASE_CONNECTION_STRING)

# create a configured "Session" class
Session = scoped_session(sessionmaker(bind=engine), scopefunc=get_current_request)
