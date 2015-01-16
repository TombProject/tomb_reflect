from pyramid.httpexceptions import HTTPNotFound


class Routes(object):
    def __init__(self, request):
        self.request = request
        self.route_manager = request.registry.route_manager

    def index(self):
        return dict(
            (route.name, {'route_pattern': route.pattern})
            for route in self.route_manager.get_routes()
        )

    def show(self):
        """This returns info about a route."""

        route_name = self.request.matchdict['route_name']

        route = self.route_manager.get_route(route_name)
        if not route:
            raise HTTPNotFound(
                'The route with name %r could not be found' % route_name)
        view_name = self.route_manager.get_view_name(route_name)

        return {
            'route_name': route.name,
            'route_pattern': route.pattern,
            'view': view_name,
        }
