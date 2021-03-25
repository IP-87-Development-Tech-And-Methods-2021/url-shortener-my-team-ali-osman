import ujson as json

from url_shortener.views import setup_routes
from url_shortener.config import Config

from url_shortener.storage import InMemoryStorage
from url_shortener.logic import Logic
from url_shortener.auth import TokenAuthenticationPolicy

from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.renderers import JSON


class UJSONRenderer(JSON):
    """Custom JSON Renderer for greater performance. You do not need to edit it"""
    def __init__(self, adapters=(), **kw):
        super().__init__(serializer=json.dumps, adapters=adapters, **kw)

    def __call__(self, info):
        """Returns a plain JSON-encoded string with content-type
        ``application/json``. The content-type may be overridden by
        setting ``request.response.content_type``."""

        def _render(value, system):
            request = system.get('request')
            if request is not None:
                response = request.response
                ct = response.content_type
                if ct == response.default_content_type:
                    response.content_type = 'application/json'
            return self.serializer(value, **self.kw)

        return _render


def make_app(app_config: Config):
    """ This function creates application instance from app_config given"""
    config = Configurator()

    # replacing standard renderer with faster one
    config.add_renderer('json', UJSONRenderer())

    # configure endpoints in the application
    setup_routes(config)

    # setup "global" objects into the registry
    storage = InMemoryStorage()

    config.registry.base_url: str = app_config.base_url
    config.registry.logic = Logic(storage=storage)

    # Setup authentication and authorization from `.auth` module
    config.set_authentication_policy(TokenAuthenticationPolicy())
    config.set_authorization_policy(ACLAuthorizationPolicy())

    # create app
    app = config.make_wsgi_app()
    return app
