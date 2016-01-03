# from collections import OrderedDict

from pyramid import testing
from pyramid_sacrud import CONFIG_MODELS
from pyramid_sacrud.views import home_view


class Foo:
    pass


class TestHome(object):

    def test_no_models(self):
        request = testing.DummyRequest()
        request.registry.settings = {}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': None}

    def test_empty_of_models(self):
        request = testing.DummyRequest()
        request.registry.settings = {CONFIG_MODELS: None}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': None}

    def test_empty_list_of_models(self):
        request = testing.DummyRequest()
        request.registry.settings = {CONFIG_MODELS: []}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': []}

    def test_with_models(self):
        request = testing.DummyRequest()
        request.registry.settings = {CONFIG_MODELS: [("foo", Foo)]}
        assert home_view(request) ==\
            {'dashboard_row_len': 3, 'resources': [("foo", Foo)]}


class TestHomeFunc(object):

    def test_200(self, testapp):
        testapp.get('/sacrud/', status=200)
        assert True
