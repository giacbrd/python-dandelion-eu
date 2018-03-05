.. image:: https://travis-ci.org/SpazioDati/python-dandelion-eu.png?branch=master
  :target: https://travis-ci.org/SpazioDati/python-dandelion-eu

.. image:: https://coveralls.io/repos/SpazioDati/python-dandelion-eu/badge.png?branch=master
  :target: https://coveralls.io/r/SpazioDati/python-dandelion-eu?branch=develop

.. image:: https://img.shields.io/pypi/v/dandelion-eu.svg
    :target: https://crate.io/packages/dandelion-eu/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/dandelion-eu.svg
    :target: https://crate.io/packages/dandelion-eu/
    :alt: Number of PyPI downloads

.. _PyPI: https://pypi.python.org/pypi/dandelion-eu/
.. _ReadTheDocs: http://python-dandelion-eu.readthedocs.org/
.. _dandelion: https://dandelion.eu/accounts/register/?next=/
.. _dandelion.eu: http://dandelion.eu/

python-dandelion-eu
===================

Bring the power of the dandelion.eu_ semantic and datagem API to your python applications and scripts!
Semantic in python couldn't be easier.


.. code-block:: py

    >>> from dandelion import DataTXT
    >>> datatxt = DataTXT(app_id='YOUR_APP_ID', app_key='YOUR_APP_KEY')
    >>> response = datatxt.nex('The doctor says an apple is better than an orange')
    >>> for annotation in response.annotations:
          print annotation
    ...

Register on dandelion_ to obtain your authentication keys and enrich your application with our semantic intelligence.

Installation
------------

``dandelion-eu`` is available on PyPI_ install it simply with::

    pip install dandelion-eu


Documentation
-------------

Documentation is available on ReadTheDocs_.
