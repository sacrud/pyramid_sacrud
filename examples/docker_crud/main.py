from zope.interface import implementer
from docker import Client

from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid_sacrud import PYRAMID_SACRUD_VIEW
from pyramid_sacrud.interfaces import ISacrudResource
from paginate import Page


@implementer(ISacrudResource)
class Docker(object):

    breadcrumb = True

    def __init__(self):
        self.cli = Client(base_url='unix://var/run/docker.sock')

    @property
    def verbose_name(self):
        return self.__class__.__name__ + "'s"

    @property
    def __name__(self):
        return self.verbose_name


class Container(Docker):

    def get_id(self, row):
        return row['Id']

    @property
    def all(self):
        return self.cli.images()


@view_config(
    context=Docker,
    renderer='sacrud/crud/list.jinja2',
    route_name=PYRAMID_SACRUD_VIEW
)
def admin_docker_list_view(context, request):
    return {
        'paginator': Page(
            context.all,
            url_maker=lambda p: request.path_url + "?page=%s" % p,
            page=int(request.params.get('page', 1)),
            items_per_page=6
        )
    }

if __name__ == '__main__':
    config = Configurator()

    # Setting up pyramid_sacrud
    config.include('pyramid_sacrud', route_prefix='admin')
    settings = config.get_settings()
    settings['pyramid_sacrud.models'] = (
        ('Docker', [Container(), ]),
    )

    # Make app
    config.scan('.')
    app = config.make_wsgi_app()

    # Start app
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
