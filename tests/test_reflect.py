from pyramid import testing
from webtest import TestApp


def _make_config():
    config = testing.setUp()
    config.include('tomb_routes')
    return config


def _make_app(config=None):
    if config is None:
        config = _make_config()

    app = config.make_wsgi_app()
    return TestApp(app)


def test_stuff():
    from tests.simple_app import my_view

    config = _make_config()
    config.add_simple_route('/path/to/view', my_view, renderer='json')

    config.include('tomb_reflect', route_prefix='/api_info')
    config.tomb_reflect_add_views()

    response = _make_app(config).get('/api_info/routes', status=200)

    assert response.content_type == 'application/json'

    route_info = (response.json.get('my_view')             # New tomb_routes
                  or response.json.get('/path/to/view'))   # Old tomb_routes
    assert route_info['route_pattern'] == '/path/to/view'

    route_info = response.json['tomb_reflect.routes#index']
    assert route_info['route_pattern'] == 'api_info/routes'

    route_info = response.json['tomb_reflect.routes#show']
    assert route_info['route_pattern'] == 'api_info/routes/{route_name}'
