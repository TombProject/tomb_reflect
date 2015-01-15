"""
tomb_reflect

Make your API introspectable
"""

from .routemanager import RouteManager


URL_PATTERNS_TO_ACTIONS = {
    '/routes':               'index',
    '/routes/{route_name}':  'show',
}
ACTIONS = URL_PATTERNS_TO_ACTIONS.values()


def route_name_for_action(action):
    return 'tomb_reflect.routes#' + action


def tomb_reflect_add_views(config, *args, **kwargs):
    if not kwargs.get('renderer'):
        kwargs['renderer'] = 'json'

    for action in ACTIONS:
        config.add_view(
            'tomb_reflect.views.Routes', attr=action,
            route_name=route_name_for_action(action),
            *args, **kwargs)


def includeme(config):
    config.registry.route_manager = RouteManager(config)

    for url_pattern, action in URL_PATTERNS_TO_ACTIONS.items():
        route_name = route_name_for_action(action)
        config.add_route(name=route_name, pattern=url_pattern)

    # Client can do: config.tomb_reflect_add_views()
    # They can also add parameters for auth, etc.
    config.add_directive('tomb_reflect_add_views', tomb_reflect_add_views)
