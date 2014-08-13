# -*- coding: utf-8 -*-
"""
action.py tests
"""

import glob
import os
import unittest

import transaction
from sqlalchemy import create_engine, orm, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Enum, Float, Integer, String, Text
from zope.sqlalchemy import ZopeTransactionExtension

from sacrud.exttype import FileStore

Base = declarative_base()

DBSession = orm.scoped_session(
    orm.sessionmaker(extension=ZopeTransactionExtension(),
                     expire_on_commit=False))

DIRNAME = os.path.dirname(__file__)
PHOTO_PATH = os.path.join(DIRNAME)


DB_FILE = os.path.join(os.path.dirname(__file__), 'test.sqlite')
TEST_DATABASE_CONNECTION_STRING = 'sqlite:///%s' % DB_FILE


class MockCGIFieldStorage(object):
    pass


class BaseSacrudTest(unittest.TestCase):
    def user_add(self):
        user = User(u'Vasya', u'Pupkin', u"123")
        self.session.add(user)
        transaction.commit()
        user = self.session.query(User).get(1)
        return user

    # def profile_add(self, user):
    #     profile = Profile(user=user)
    #     self.session.add(profile)
    #     transaction.commit()
    #     profile = self.session.query(Profile).first()
    #     return profile

    def setUp(self):

        engine = create_engine('sqlite:///:memory:')
        DBSession.remove()
        DBSession.configure(bind=engine)

        session = DBSession
        self.session = session

        # To create tables, you typically do:
        User.metadata.create_all(engine)
        Profile.metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()

        def clear_files():
            files = glob.glob("%s/*.html" % PHOTO_PATH)
            files += glob.glob("%s/*.txt" % PHOTO_PATH)
            for filename in files:
                os.remove(os.path.join(PHOTO_PATH, filename))
        clear_files()


association_table = Table('association', Base.metadata,
                          Column('group_id', Integer, ForeignKey('group.id')),
                          Column('user_id', Integer, ForeignKey('user.id'))
                          )


class Groups(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship("User", secondary=association_table)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String, info={'verbose_name': 'user password'})
    sex = Column(Enum('male',
                      'female',
                      'alien',
                      'unknown', name="sex"))

    groups = relationship("Groups", secondary=association_table)

    def __init__(self, name, fullname, password, sex='unknown'):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.sex = sex


class Profile(Base):

    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship(User, backref=backref("profile", lazy="joined"))
    phone = Column(String)
    cv = Column(Text)
    married = Column(Boolean)
    salary = Column(Float)
    photo = Column(FileStore(path="/assets/photo", abspath=PHOTO_PATH))

    def __init__(self, user, phone="", cv="", married=False, salary=20.0):
        self.user = user
        self.phone = phone
        self.cv = cv
        self.married = married
        self.salary = salary
