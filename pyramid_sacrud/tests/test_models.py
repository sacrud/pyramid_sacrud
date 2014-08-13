#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Models for SACRUD tests
"""
import transaction
from sqlalchemy import create_engine

from pyramid_sacrud.tests import Base, DBSession, TEST_DATABASE_CONNECTION_STRING, User


def user_add(session):
    user = User(u'Vasya', u'Pupkin', u"123")
    session.add(user)
    transaction.commit()
    user = session.query(User).get(1)
    return user


def _initTestingDB(url=TEST_DATABASE_CONNECTION_STRING):
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    return DBSession
