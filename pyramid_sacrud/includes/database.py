#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Database settings
"""
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from sacrud import crud_sessionmaker


def includeme(config):
    engine = sqlalchemy.engine_from_config(config.registry.settings)
    DBSession = crud_sessionmaker(scoped_session(
        sessionmaker(extension=ZopeTransactionExtension())))
    DBSession.configure(bind=engine)
    config.add_request_method(lambda x: DBSession, 'dbsession', reify=True,
                              property=True)
