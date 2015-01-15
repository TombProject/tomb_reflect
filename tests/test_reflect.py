from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound
from pytest import raises
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


def test_routes_index():
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


def test_routes_show_imperative():
    from tests.simple_app import my_view

    config = _make_config()
    config.add_simple_route('/path/to/view', my_view, renderer='json')

    config.include('tomb_reflect', route_prefix='/api_info')
    config.tomb_reflect_add_views()

    response = _make_app(config).get('/api_info/routes', status=200)
    assert response.content_type == 'application/json'

    for route_name in ('my_view', '/path/to/view'):
        if route_name in response.json.keys():
            break

    response = _make_app(config).get(
        '/api_info/routes/{route_name}'.format(route_name=route_name),
        status=200)

    assert response.content_type == 'application/json'
    assert response.json['route_pattern'] == '/path/to/view'
    assert response.json['route_name'] == 'my_view'
    assert response.json['view'] == 'tests.simple_app.my_view'


def test_routes_show_declarative():
    config = _make_config()
    config.scan('tests.simple_app')

    config.include('tomb_reflect', route_prefix='/api_info')
    config.tomb_reflect_add_views()

    response = _make_app(config).get(
        '/api_info/routes/decorated_view',
        status=200)

    assert response.content_type == 'application/json'
    assert response.json['route_pattern'] == '/path/to/decorated/view/func'
    assert response.json['route_name'] == 'decorated_view'
    assert response.json['view'] == 'tests.simple_app.decorated_view'


def test_routes_show_class_method():
    config = _make_config()
    config.scan('tests.simple_app')

    config.include('tomb_reflect', route_prefix='/api_info')
    config.tomb_reflect_add_views()

    response = _make_app(config).get(
        '/api_info/routes/MyViewsClass.imperative_view',
        status=200)

    assert response.content_type == 'application/json'
    assert response.json['route_pattern'] == '/path/to/decorated/view/method'
    assert response.json['route_name'] == 'MyViewsClass.imperative_view'
    assert 'imperative_view' in response.json['view']


def test_routes_show_route_not_found():
    config = _make_config()
    config.include('tomb_reflect', route_prefix='/api_info')
    config.tomb_reflect_add_views()

    with raises(HTTPNotFound):
        _make_app(config).get(
            '/api_info/routes/XYZ_route_not_found_XYZ',
            status=404)


def test_routes_show_route_with_no_view():
    route_name = 'route_with_no_view'
    path = '/route_with_no_view'
    config = _make_config()
    config.add_route(route_name, path)
    config.include('tomb_reflect', route_prefix='/api_info')
    config.tomb_reflect_add_views()

    response = _make_app(config).get(
        '/api_info/routes/route_with_no_view',
        status=200)

    assert response.content_type == 'application/json'
    assert response.json['route_pattern'] == '/route_with_no_view'
    assert response.json['route_name'] == 'route_with_no_view'
    assert response.json['view'] is None
