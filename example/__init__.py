from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return self.name


class Manufacturer(Base):
    __tablename__ = 'manufacturers'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))
    manufacturer = relationship('Manufacturer',
                                backref=backref('cars', lazy='dynamic'))


def sacrud_settings(config):
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = (
        ('Vehicle', [Manufacturer, Car]),
        ('Group2', [User])
    )


def database_settings(config):
    from sqlalchemy import create_engine
    config.registry.settings['sqlalchemy.url'] = db_url =\
        "sqlite:///example.db"
    engine = create_engine(db_url)
    Base.metadata.bind = engine
    Base.metadata.create_all()


def main(global_settings, **settings):
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')

    config = Configurator(
        settings=settings,
        session_factory=my_session_factory,
    )

    config.include(database_settings)
    config.include(sacrud_settings)
    return config.make_wsgi_app()


if __name__ == '__main__':
    settings = {
        'auth.secret': 'seekrit',
    }
    app = main({}, **settings)

    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
