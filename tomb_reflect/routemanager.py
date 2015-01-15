class RouteManager(object):
    def __init__(self, config):
        self.route_mapper = config.get_routes_mapper()
        self.introspector = config.introspector

    def get_routes(self):
        for route in self.route_mapper.get_routes():
            route.pattern = route.pattern.replace('{optional_slash:/?}', '')
            yield route

    def get_route(self, route_name):
        for route in self.get_routes():
            if route.name == route_name:
                return route

    def get_view_name(self, route_name):
        view_func = self.get_view_func(route_name)

        if view_func:
            return self.get_function_name(view_func)
        else:
            return None

    def get_view_func(self, route_name):
        route_intr = self.introspector.get('routes', route_name)

        if not route_intr:
            return None

        for related in self.introspector.related(route_intr):
            if related.category_name == 'views':
                if related['attr']:
                    return getattr(related['callable'], related['attr'])
                else:
                    return related['callable']

    def get_function_name(self, obj):
        # obj could be a method or a function
        if hasattr(obj, '__qualname__'):  # a method in Python 3
            return '%s.%s' % (
                obj.__module__, obj.__qualname__)
        if hasattr(obj, 'im_class'):  # a method in Python 2
            return '%s.%s.%s' % (
                obj.__module__, obj.im_class.__name__, obj.__name__)
        else:  # a function
            return '%s.%s' % (
                obj.__module__, obj.__name__)
