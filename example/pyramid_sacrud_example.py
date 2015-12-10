from sqlalchemy import Column, String, Boolean, Integer, Unicode, ForeignKey
from pyramid.config import Configurator
from sqlalchemy.orm import backref, relationship, sessionmaker, scoped_session
from pyramid.session import SignedCookieSessionFactory
from pyramid.security import Allow, forget, remember
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.httpexceptions import HTTPFound
from pyramid_sacrud import PYRAMID_SACRUD_HOME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    name = Column(String(30), primary_key=True)

    def __repr__(self):
        return self.name


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return self.name


class Good(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Group', backref='goods')

    visible = Column(Boolean, default=False)
    archive = Column(Boolean)

    def __repr__(self):
        return self.name


class Parent(Base):
    __tablename__ = 'parents'

    slug = Column(Unicode, primary_key=True)
    name = Column(Unicode, nullable=False)


class Child(Base):
    __tablename__ = 'children'

    provider_slug = Column(Unicode, ForeignKey('parents.slug'),
                           primary_key=True)
    slug = Column(Unicode, primary_key=True)

    provider = relationship('Parent', backref=backref('children'))


class GroupName(object):

    def __init__(self, label, name):
        self.name = name
        self.label = label if label else name

    def __repr__(self):
        return self.name


def sacrud_settings(config):
    config.include('ps_alchemy')
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = (
        ('Catalouge', [Group, Good]),
        (GroupName('Auth system', 'auth'), [User]),
        ('', []),
        ('foo', [Parent, Child])
    )


def database_settings(config):
    from sqlalchemy import engine_from_config
    settings = config.registry.settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()


def add_fixtures():
    for id, user_name in enumerate(('admin', 'moderator', 'user1', 'user2')):
        DBSession.add(User(name=user_name, id=id))
    for group_name in ('Electronics', 'Fashion', 'Home & Garden', 'Motors'):
        group = Group(name=group_name)
        DBSession.add(group)
        if group_name == 'Electronics':
            DBSession.add(Good(name='iPhone', group=group))
            DBSession.add(Good(name='Fridge', group=group))
            DBSession.add(Good(name='YotaPhone', group=group))
        elif group_name == 'Fashion':
            DBSession.add(Good(name='Jeans', group=group))
        elif group_name == 'Home & Garden':
            DBSession.add(Good(name='Rake', group=group))
        elif group_name == 'Motors':
            DBSession.add(Good(name='Chevrolet Cavalier', group=group))
            DBSession.add(Good(name='LADA Granta', group=group))
    DBSession.commit()


class Root(object):
    __acl__ = [(Allow, 'admin', PYRAMID_SACRUD_HOME), ]

    def __init__(self, request):
        self.request = request


def login(request):
    headers = remember(request, 'admin')
    return HTTPFound(location=request.route_url(PYRAMID_SACRUD_HOME),
                     headers=headers)


def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url(PYRAMID_SACRUD_HOME),
                     headers=headers)


def main(global_settings, **settings):
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    config = Configurator(
        settings=settings,
        session_factory=my_session_factory,
    )
    if 'auth' in settings:
        authn_policy = AuthTktAuthenticationPolicy(
            'sosecret',
            callback=lambda u, r: ['admin', ],
        )
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(ACLAuthorizationPolicy())
        config.set_root_factory(Root)

        config.add_route('login', '/login')
        config.add_route('logout', '/logout')
        config.add_view(login, route_name='login')
        config.add_view(logout, route_name='logout')

    config.include(database_settings)
    config.include(sacrud_settings)

    if 'fixtures' in settings:
        add_fixtures()
    return config.make_wsgi_app()


if __name__ == '__main__':
    settings = {
        'sqlalchemy.url': 'sqlite:///example.sqlite',
        'fixtures': True,
    }
    app = main({}, **settings)

    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=6543)
    except ImportError:
        from wsgiref.simple_server import make_server
        server = make_server('0.0.0.0', 6543, app)
        server.serve_forever()
