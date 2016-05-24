from pyramid.view import view_config
from pyramid.config import Configurator
from zope.interface import implementer
from pyramid.security import Allow, Everyone
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy

from pyramid_sacrud import PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_VIEW
from pyramid_sacrud.interfaces import ISacrudResource

authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
authz_policy = ACLAuthorizationPolicy()


@implementer(ISacrudResource)
class Bear(object):

    breadcrumb = True

    __acl__ = [
        (Allow, Everyone, PYRAMID_SACRUD_VIEW),
    ]

    def __init__(self, name, url=None):
        self.name = name
        self.url = url

    @property
    def verbose_name(self):
        return self.name

    @property
    def __name__(self):
        return self.verbose_name


@view_config(
    context=Bear,
    renderer='bear.jinja2',
    route_name=PYRAMID_SACRUD_VIEW,
    permission=PYRAMID_SACRUD_VIEW
)
def admin_bear_view(context, request):
    return {}


class BearFactory(object):

    def __init__(self, request):
        self.__acl__ = [
            (Allow, Everyone, PYRAMID_SACRUD_HOME),
        ]


if __name__ == '__main__':
    config = Configurator(root_factory=BearFactory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # Setting up pyramid_sacrud
    config.include('pyramid_sacrud', route_prefix='admin')
    settings = config.get_settings()
    settings['pyramid_sacrud.models'] = (
        ('Bears', [
            Bear(
                'Brown',
                'http://i.imgur.com/D5SBanK.jpg'
            ),
            Bear(
                'Panda',
                'http://i.imgur.com/uiJWAf3.jpg'
            ),
            Bear(
                'Polar',
                'http://i.imgur.com/j5SDeeH.jpg'
            )
        ]),
    )

    # Make app
    config.scan('.')
    app = config.make_wsgi_app()

    # Start app
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
