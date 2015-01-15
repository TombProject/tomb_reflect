tomb_reflect
=================================

Intro
=================================

Easily make your Pyramid-powered Web API introspectable.

All it takes is:

.. code-block:: python

   config.include('tomb_reflect', route_prefix='/api_info')

    # You could pass options to tomb_reflect_add_views to add auth, etc.
    config.tomb_reflect_add_views()

With this, your app now responds to 2 new URLs.

The first URL, ``/api_info/routes``, returns a list of routes:

.. code-block:: json

    {
        "hello": {
            "route_pattern": "/hello"
        },
        "hello_name": {
            "route_pattern": "/hello_name/{name}"
        },
        "tomb_reflect.routes#index": {
            "route_pattern": "api_info/routes"
        },
        "tomb_reflect.routes#show": {
            "route_pattern": "api_info/routes/{route_name}"
        }
    }

The second URL, ``/api_info/routes/{route_name}``, returns detailed info for a
specific route:

.. code-block:: json

    {
        "route_name": "hello",
        "route_pattern": "/hello",
        "view": "inventorysvc.views.hello.hello"
    }


Configuration
=================================

If you want the URLs to be under a different root path, change the
``route_prefix`` in your ``config.include`` call:

.. code-block:: python

   config.include('tomb_reflect', route_prefix='/super/secret/place')

If you want the URLs to only be visible with certain permissions, require
special authorization, etc., you can pass options to
``config.tomb_reflect_add_views``:

.. code-block:: python

    # You can pass options to tomb_reflect_add_views to add auth, etc.
    config.tomb_reflect_add_views(
        decorator=SomeCustomDecorator,
        permission='reflect')


Similar
=================================

- pyramid-describe_ - Only works for apps that use pyramid-controller_ dispatch though


.. _Pyramid: http://www.trypyramid.com/
.. _pyramid-describe: https://pypi.python.org/pypi/pyramid_describe
.. _pyramid-controller: https://pypi.python.org/pypi/pyramid_controllers
