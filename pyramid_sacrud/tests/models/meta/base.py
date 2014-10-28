from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pyramid.threadlocal import get_current_request
from sqlalchemy import engine_from_config, MetaData
from logging.config import fileConfig
from ConfigParser import SafeConfigParser
from decorator import decorator
from .schema import References

def setup_app(global_config, **settings):
    """Called when the Pyramid app first runs."""

    # produce a database engine from the config.
    all_settings = global_config.copy()
    all_settings.update(settings)
    setup(all_settings)

def setup_from_file(fname):
    """Setup the model from a config file name.

    This is used for unit tests and console scripts.

    TODO: if there's way to get this from the Pyramid configurator,
    that might be better.

    """
    fileConfig(fname)
    config = SafeConfigParser()
    config.read(fname)

    settings = dict(config.items("DEFAULT"))
    setup(settings)

engine = None

def setup(config):
    """Setup the application given a config dictionary."""

    global engine
    engine = engine_from_config(config, "sqlalchemy.")
    Session.configure(bind=engine)

@decorator
def commit_on_success(fn, *arg, **kw):
    """Decorate any function to commit the session on success, rollback in
    the case of error."""

    try:
        result = fn(*arg, **kw)
        Session.commit()
    except:
        Session.rollback()
        raise
    else:
        return result

# bind the Session to the current request
# Convention within Pyramid is to use the ZopeSQLAlchemy extension here,
# allowing integration into Pyramid's transactional scope.
Session = scoped_session(sessionmaker(), scopefunc=get_current_request)

class Base(References):
    pass

Base = declarative_base(cls=Base)

# establish a constraint naming convention.
# see http://docs.sqlalchemy.org/en/latest/core/constraints.html#configuring-constraint-naming-conventions
#
Base.metadata.naming_convention={
        "pk": "pk_%(table_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ix": "ix_%(table_name)s_%(column_0_name)s"
    }