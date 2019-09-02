.. _dashboard: https://dandelion.eu/profile/dashboard/
.. _dandelion.eu: https://dandelion.eu/

General Documentation
=====================

What is explained here applies to all the services available in this package.
For specific documentation on each service, please refer to their page.

Authentication
--------------
Most (all?) of the dandelion.eu_ services require authentication. You can
find your authentication token on your dashboard_ and pass them to the class
constructor, for example::

    >>> from dandelion import DataTXT
    >>> administrative_regions = DataTXT(token='8697xxxx8b99xxxxeecbxxxxb163xxxx')


If you need to instantiate more services, you can specify your authentication
token just once using ``dandelion.default_config``::

    >>> from dandelion import default_config
    >>> default_config['token'] = '8697xxxx8b99xxxxeecbxxxxb163xxxx'

    >>> from dandelion import DataTXT
    >>> datatxt = DataTXT()


The old authentication system by `app_id` and `app_key` does not work anymore,
but it is still possible to use these parameters by setting the token value on both.

Caching your queries
--------------------
To avoid wasting units (and time) you can easily cache all your requests
using the classes provided by the ``dandelion.cache`` package. Currently
just ``FileCache`` is available, but more can be easily implemented using
the abstract cache class.

To enable caching, instantiate a cache object and pass it to the services
you need::

    >>> from dandelion import DataTXT
    >>> from dandelion.cache import FileCache
    >>> datatxt = DataTXT(cache=FileCache('.cache_dir'))
