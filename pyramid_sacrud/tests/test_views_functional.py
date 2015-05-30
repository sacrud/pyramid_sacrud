#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Functional tests for views
"""
import transaction
from sqlalchemy.exc import IntegrityError
from webtest import TestApp

from ._mock_main import main
from .models import TEST_DATABASE_CONNECTION_STRING, Session
from .models.auth import Groups, User
from .test_views import _TransactionalFixture


class PyramidApp(_TransactionalFixture):
    def setUp(self):
        super(PyramidApp, self).setUp()
        settings = {'sqlalchemy.url': TEST_DATABASE_CONNECTION_STRING}
        app = main({}, **settings)
        self.testapp = TestApp(app)


class HomeFuncTests(PyramidApp):

    def test_sa_home(self):
        res = self.testapp.get('/admin/', status=200)
        self.failUnless('Auth models' in str(res.body))
        self.failUnless('user' in str(res.body))
        self.failUnless('profile' in str(res.body))


class CreateFuncTests(PyramidApp):

    def test_sa_create(self):
        self._create_tables()
        self.testapp.get('/admin/user/create/', status=200)

    def test_sa_create_table_not_exist(self):
        self.testapp.get('/admin/not_exist_table/create/', status=404)
        self.assertEqual(self._is_table_exist('not_exist_table'), False)

    def test_sa_create_post(self):
        self._create_tables()
        self.testapp.post('/admin/user/create/',
                          {'form.submitted': '1',
                           'name': u'foo bar baz'},
                          status=302)
        user = Session.query(User).order_by(User.id.desc()).first()
        self.assertEqual(user.name, 'foo bar baz')

    def test_sa_create_update_none_repr_obj(self):
        self._create_tables()
        self.testapp.post('/admin/group/create/',
                          {'form.submitted': '1'},
                          status=302)
        group = Session.query(Groups).order_by(Groups.id.desc()).count()
        self.assertLess(0, group)

        self.testapp.post('/admin/group/update/id/1',
                          {'form.submitted': '1',
                           'id': 2},
                          status=302)
        self.assertLess(0, group)

    def test_sa_create_an_existing_obj(self):
        self._create_tables()
        self.testapp.post('/admin/group/create/',
                          {'id': 1, 'form.submitted': '1'},
                          status=302)
        group = Session.query(Groups).order_by(Groups.id.desc()).count()
        self.assertLess(0, group)
        self.assertRaises(
            IntegrityError, self.testapp.post,
            '/admin/group/create/',
            {'id': 1, 'form.submitted': '1'},
            status=302
        )


class ReadFuncTests(PyramidApp):

    def test_sa_list(self):
        self._create_tables()
        self.testapp.get('/admin/user/', status=200)
        self.testapp.get('/admin/profile/', status=200)


class UpdateFuncTests(PyramidApp):

    def test_sa_update(self):
        self._user_fixture()
        self.testapp.get('/admin/user/update/id/1', status=200)

    def test_sa_update_not_found(self):
        self._create_tables()
        self.testapp.get('/admin/user/update/id/100500', status=404)

    def test_sa_update_bad_pk(self):
        self._create_tables()
        self.testapp.get('/admin/user/update/', status=404)
        self.testapp.get('/admin/user/update/id', status=404)
        self.testapp.get('/admin/user/update/not_pk/1', status=404)
        self.testapp.get('/admin/user/update/id/1/foo/2', status=404)

    def test_sa_update_table_not_exist(self):
        self.testapp.get('/admin/not_exist_table/update/id/100500', status=404)
        self.assertEqual(self._is_table_exist('not_exist_table'), False)

    def test_sa_update_post(self):
        self._user_fixture()
        self.testapp.post('/admin/user/update/id/1',
                          {'form.submitted': '1',
                           'name': 'foo bar baz'},
                          status=302)
        user = Session.query(User).filter_by(id=1).one()
        self.assertEqual(user.name, 'foo bar baz')

    def test_sa_update_post_bad_data(self):
        self._user_fixture()
        self.testapp.post('/admin/user/update/id/1',
                          {'form.submitted': '1', },
                          status=302)
        user = Session.query(User).filter_by(id=1).one()
        self.assertEqual(user.name, 'some user 1')


class DeleteFuncTests(PyramidApp):

    def test_delete_user(self):
        self._user_fixture()
        self.testapp.get('/admin/user/delete/id/1', status=302)
        user = Session.query(User).filter_by(id=1).all()
        self.assertEqual(len(user), 0)

    def test_delete_not_found_user(self):
        self._create_tables()
        self.testapp.get('/admin/user/delete/id/100500', status=404)
        user = Session.query(User).filter_by(id=100500).all()
        self.assertEqual(len(user), 0)

    def test_sa_delete_bad_pk(self):
        self._create_tables()
        self.testapp.get('/admin/user/delete/', status=404)
        self.testapp.get('/admin/user/delete/id', status=404)
        self.testapp.get('/admin/user/delete/not_pk/1', status=404)
        self.testapp.get('/admin/user/delete/id/1/foo/2', status=404)

    def test_delete_not_exist_table(self):
        self._create_tables()
        self.testapp.get('/admin/not_exist_table/delete/id/1', status=404)
        self.assertEqual(self._is_table_exist('not_exist_table'), False)

    def test_sa_list_delete_actions(self):
        ids = range(1, 100)
        self._user_fixture(ids=ids)
        deleted_ids = range(11, 25)
        items_list = [u'["id", %s]' % id for id in deleted_ids]
        self.testapp.post('/admin/user/',
                          {'selected_action': 'delete',
                           'selected_item': items_list},
                          status=302)
        transaction.commit()
        count = Session.query(User).filter(
            User.id.in_(deleted_ids)).count()
        self.assertEqual(count, 0)
        count = Session.query(User).filter(
            User.id.in_(ids)).count()
        self.assertEqual(count, len(ids) - len(deleted_ids))
