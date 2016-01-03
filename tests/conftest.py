import pytest
from webtest import TestApp
from pyramid.config import Configurator
from pyramid.response import Response


def test_app():

    def hello(request):
        return Response('Hello world!')

    config = Configurator()
    config.add_route('hello_world', '/')
    config.add_view(hello, route_name='hello_world')
    config.include('pyramid_sacrud')
    return config.make_wsgi_app()


@pytest.fixture(scope="function")
def testapp(request):
    app = test_app()
    return TestApp(app)
