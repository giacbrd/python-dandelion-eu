.. _dashboard: https://dandelion.eu/profile/dashboard/
.. _dandelion.eu: https://dandelion.eu/

General Documentation
=====================

What is explained here applies to all the services available in this package.
For specific documentation on each service, please refer to their page.

Authentication
--------------
Most (all?) of the dandelion.eu_ services require authentication. You can
find your authentication token on your dashboard_ and pass it to the class
constructor, for example::

    >>> from dandelion import Datagem
    >>> administrative_regions = Datagem('administrative-regions',
    ...                                  token='7682xxxxxeh2nb2v2mxxxxxxxjh9sbxxxx')


If you need to instantiate more services, you can specify your authentication
token just once using ``dandelion.default_config`` ::

    >>> from dandelion import default_config
    >>> default_config['token'] = '7682xxxxxeh2nb2v2mxxxxxxxjh9sbxxxx'

    >>> from dandelion import DataTXT, Datagem, Sentiment
    >>> datatxt = DataTXT()
    >>> administrative_regions = Datagem('administrative-regions')
    >>> sentiment = Sentiment()

Legacy authentication system
----------------------------
The client still supports authentication through ``$app_id`` and ``$app_key`` .
The use is the same as for the token: you can pass ``app_id`` and ``app_key``
to the class contructor or specify them once using ``dandelion.default_config`` ::

    >>> from dandelion import Datagem
    >>> administrative_regions = Datagem('administrative-regions',
    ...                                  app_id='24cxxxx',
    ...                                  app_key='8697xxxx8b99xxxxeecbxxxxb163xxxx')

                                        OR

    >>> from dandelion import default_config
    >>> default_config['app_id'] = '24cxxxx'
    >>> default_config['app_key'] = '8697xxxx8b99xxxxeecbxxxxb163xxxx'

    >>> from dandelion import DataTXT, Datagem, Sentiment
    >>> datatxt = DataTXT()
    >>> administrative_regions = Datagem('administrative-regions')
    >>> sentiment = Sentiment()

Notes on authentication
-----------------------
You have to specify the ``token`` OR the pair (``app_id``, ``app_key``): if you specify
them both, the client will raise an exception.

Moreover, the client will use what is stored in ``default_config`` only if you
don't pass anything to the class constructor.

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
