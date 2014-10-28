"""Mock SQLAlchemy Session recipe.

Worked out with help from Michael Foord.

"""
import mock

from sqlalchemy.sql import visitors
from sqlalchemy.sql.expression import ClauseElement, BindParameter, literal_column


class MockSession(mock.MagicMock):
    def __init__(self, *arg, **kw):
        kw.setdefault('side_effect', self._side_effect)
        super(MockSession, self).__init__(*arg, **kw)
        self._lookup = {}
        self.info = {}   # Session.info dict

    def _side_effect(self, *arg, **kw):
        if self._mock_return_value is not mock.sentinel.DEFAULT:
            return self._mock_return_value
        else:
            return self._generate(*arg, **kw)

    def _get_key(self, arg, kw):
        return tuple(self._hash(a) for a in arg) + \
            tuple((k, self._hash(kw[k])) for k in sorted(kw))

    def _literal_sql_parameter(self, value):
        return "'%s'" % value

    def _hash(self, arg):
        if isinstance(arg, ClauseElement):
            def _replace(arg):
                if isinstance(arg, BindParameter):
                    return literal_column(
                        self._literal_sql_parameter(arg.effective_value)
                    )
            convert_binds = visitors.replacement_traverse(arg, {}, _replace)
            expr = str(convert_binds)
            return expr
        else:
            assert hash(arg)
            return arg

    def _generate(self, *arg, **kw):
        key = self._get_key(arg, kw)
        if key in self._lookup:
            return self._lookup[key]
        else:
            self._lookup[key] = ret = MockSession()
            return ret
