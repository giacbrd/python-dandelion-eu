.. image:: https://travis-ci.org/giacbrd/python-dandelion-eu.svg?branch=develop
  :target: https://travis-ci.org/giacbrd/python-dandelion-eu

.. image:: https://coveralls.io/repos/SpazioDati/python-dandelion-eu/badge.png?branch=develop
  :target: https://coveralls.io/r/SpazioDati/python-dandelion-eu?branch=develop

.. image:: https://img.shields.io/pypi/v/dandelion-eu
    :target: https://pypi.python.org/pypi/dandelion-eu/
    :alt: Latest PyPI version

.. _PyPI: https://pypi.python.org/pypi/dandelion-eu/
.. _ReadTheDocs: http://python-dandelion-eu.readthedocs.org/
.. _dandelion: https://dandelion.eu/accounts/register/?next=/
.. _dandelion.eu: http://dandelion.eu/

python-dandelion-eu
===================

Bring the power of the dandelion.eu_ semantic to your python applications and scripts!
Semantic in python couldn't be easier.


.. code-block:: py

    >>> from dandelion import DataTXT
    >>> datatxt = DataTXT(token='YOUR_TOKEN')
    >>> response = datatxt.nex('The doctor says an apple is better than an orange')
    >>> for annotation in response.annotations:
          print(annotation)
    ...

Register on dandelion_ to obtain your authentication token and enrich your application with our semantic intelligence.

Installation
------------

``dandelion-eu`` is available on PyPI_ install it simply with::

    pip install dandelion-eu


Documentation
-------------

Documentation is available on ReadTheDocs_.
