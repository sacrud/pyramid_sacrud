from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


def many_to_one(clsname, **kw):
    """Use an event to build a many-to-one relationship on a class.

    This makes use of the :meth:`.References._reference_table` method
    to generate a full foreign key relationship to the remote table.

    """
    @declared_attr
    def m2o(cls):
        cls._references((cls.__name__, clsname))
        return relationship(clsname, **kw)
    return m2o

def one_to_many(clsname, **kw):
    """Use an event to build a one-to-many relationship on a class.

    This makes use of the :meth:`.References._reference_table` method
    to generate a full foreign key relationship from the remote table.

    """
    @declared_attr
    def o2m(cls):
        cls._references((clsname, cls.__name__))
        return relationship(clsname, **kw)
    return o2m


class UniqueMixin(object):
    """Unique object mixin.

    Allows an object to be returned or created as needed based on
    criterion.

    .. seealso::

        http://www.sqlalchemy.org/trac/wiki/UsageRecipes/UniqueObject

    """
    @classmethod
    def unique_hash(cls, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def unique_filter(cls, query, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def as_unique(cls, session, *arg, **kw):

        hashfunc = cls.unique_hash
        queryfunc = cls.unique_filter
        constructor = cls

        if 'unique_cache' not in session.info:
            session.info['unique_cache'] = cache = {}
        else:
            cache = session.info['unique_cache']

        key = (cls, hashfunc(*arg, **kw))
        if key in cache:
            return cache[key]
        else:
            with session.no_autoflush:
                q = session.query(cls)
                q = queryfunc(q, *arg, **kw)
                obj = q.first()
                if not obj:
                    obj = constructor(*arg, **kw)
                    session.add(obj)
            cache[key] = obj
            return obj
