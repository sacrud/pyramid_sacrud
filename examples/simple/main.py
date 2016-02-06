from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


if __name__ == '__main__':
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    config = Configurator(session_factory=my_session_factory)

    config.include('pyramid_sacrud', route_prefix='admin')

    app = config.make_wsgi_app()

    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
