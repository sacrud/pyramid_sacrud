from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))

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

    def __repr__(self):
        return self.name


def sacrud_settings(config):
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = (
        ('Catalouge', [Group, Good]),
        ('Auth system', [User])
    )


def database_settings(config):
    from sqlalchemy import create_engine
    config.registry.settings['sqlalchemy.url'] = db_url =\
        "sqlite:///example.db"
    engine = create_engine(db_url)
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()


def add_fixtures():
    for user_name in ('admin', 'moderator', 'user1', 'user2'):
        DBSession.add(User(name=user_name))
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


def main(global_settings, **settings):
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')

    config = Configurator(
        settings=settings,
        session_factory=my_session_factory,
    )

    config.include(database_settings)
    config.include(sacrud_settings)
    if 'fixtures' in settings:
        add_fixtures()
    return config.make_wsgi_app()


if __name__ == '__main__':
    settings = {}
    app = main({}, **settings)

    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
