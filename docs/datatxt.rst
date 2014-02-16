:title:
    The dataTXT API

.. _SpazioDati: http://www.spaziodati.eu
.. _dataTXT-NEX documentation on dandelion.eu: https://dandelion.eu/docs/api/datatxt/nex/v1/
.. _dataTXT-SIM documentation on dandelion.eu: https://dandelion.eu/docs/api/datatxt/sim/v1/
.. _dataTXT-LI documentation on dandelion.eu: https://dandelion.eu/docs/api/datatxt/li/v1/


The dataTXT API
===============
dataTXT is a family of semantic services developed by SpazioDati_. All its
methods are available in the same class::

   >>> from dandelion import DataTXT
   >>> datatxt = DataTXT(app_id='', app_key='')


NEX: Named Entity Extraction
----------------------------
dataTXT-NEX is a named entity extraction & linking API that performs very well
even on short texts, on which many other similar services do not. dataTXT-NEX
currently works on Italian and English texts. With this API you will be able
to automatically tag your texts, extracting Wikipedia entities and enriching
your data.

You can extract annotated entities with::

    >>> for annotation in datatxt.nex('Oh my, arduino is super cool, so #opensource').annotations:
    ...     print(annotation.uri)
    http://en.wikipedia.org/wiki/Arduino
    http://en.wikipedia.org/wiki/Open_source


Additional parameters can be specified simply by::

    >>> result = datatxt.nex('Oh my, arduino is super cool, so #opensource',
    ...                      include_lod=True,
    ...                      )
    >>> [annotation.lod.dbpedia for annotation in result.annotations]
    ['http://dbpedia.org/resource/Arduino',
     'http://dbpedia.org/resource/Open_source']

Check out the `dataTXT-NEX documentation on dandelion.eu`_ for more information
about what can be done with NEX.


SIM: Text Similarity
--------------------
dataTXT-SIM is a semantic sentence similarity API optimized on short sentences.
With this API you will be able to compare two sentences and get a score of their
semantic similarity. It works even if the two sentences don't have any word in
common.

You can compute the semantic similarity between two texts with::

    >>> datatxt.sim('Barack Obama is the president of the US',
    ...             'Bob Iger is the CEO of Walt Disney')
    {'lang': 'en',
     'langConfidence': 1.0,
     'similarity': 0.2564,
     'time': 11,
     'timestamp': '2042-01-01T01:02:03'}


Check out the `dataTXT-SIM documentation on dandelion.eu`_ for more information
about what can be done with SIM.


LI: Language Identification
---------------------------
dataTXT-LI is a simple language identification API; it is a tool that may be
useful when dealing with texts, so we decided to open it to all our users.
It currently supports more than 50 languages.

You can identify the language of a text with::

    >>> datatxt.li('mamma mia! un testo in italiano!')
    {'detectedLangs': [{'confidence': 0.9999952605110598, 'lang': 'it'}],
     'time': 0,
     'timestamp': '2042-01-01T01:02:03'}

Check out the `dataTXT-LI documentation on dandelion.eu`_.
