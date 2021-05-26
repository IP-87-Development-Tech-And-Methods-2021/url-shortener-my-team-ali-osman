from .handlers import (
    public_resource_example,
    read_user,
    create_user,
    login_user,
    logout_user,
    notfound,
    forbidden,
)

PROTECTED = 'url_shortener.auth.protected'


def setup_routes(config):
    """ Configures application routes"""
    # Add public resources
    config.add_view(public_resource_example,
                    route_name='public_resource_example',
                    renderer='json')
    config.add_route('public_resource_example', '/public')

    # Add protected resources
    # pass `factory=PROTECTED` to the `add_route` method
    # in order to make this resource available for authenticated users only
    config.add_route('create_user',
                     request_method='POST',
                     pattern='/user/create')
    config.add_view(create_user,
                    route_name='create_user')

    config.add_route('read_user',
                     request_method='GET',
                     pattern='/user/signup/{key}',
                     factory=PROTECTED)
    config.add_view(read_user,
                    route_name='read_user',
                    permission='read')

    config.add_route('login_user',
                     request_method='POST',
                     pattern='/user')
    config.add_view(login_user,
                    route_name='login_user')

    config.add_route('logout_user',
                     request_method='POST',
                     pattern='/user/logout',
                     factory=PROTECTED)
    config.add_view(logout_user,
                    route_name='logout_user',
                    permission='read')

    # Add error views
    config.add_notfound_view(notfound)
    config.add_forbidden_view(forbidden)

    return config
