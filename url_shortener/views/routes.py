from .handlers import (
    public_resource_example,
    create_user,
    login_user,
    logout_user,
    redirect_longlink,
    create_shortlink,
    list_links_for_user,
    delete_shortlink,
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

    config.add_route('redirect_longlink',
                     request_method='GET',
                     pattern='/{id}'
                     )
    config.add_view(redirect_longlink,
                    route_name='redirect_longlink'
                    )

    config.add_route('create_shortlink',
                     request_method='POST',
                     pattern='/urls/shorten',
                     factory=PROTECTED)
    config.add_view(create_shortlink,
                    route_name='create_shortlink',
                    permission='read')

    config.add_route('list_links_for_user',
                     request_method='GET',
                     # '/urls' would be better imo but in specification it's stated as '/urls/list' for some reason
                     pattern='/urls/list',
                     factory=PROTECTED)
    config.add_view(list_links_for_user,
                    route_name='list_links_for_user',
                    permission='read')

    config.add_route('delete_shortlink',
                     request_method='POST',
                     pattern='/urls/delete',
                     factory=PROTECTED)
    config.add_view(delete_shortlink,
                    route_name='delete_shortlink',
                    permission='read')


    # Add error views
    config.add_notfound_view(notfound)
    config.add_forbidden_view(forbidden)

    return config
