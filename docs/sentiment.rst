.. _Sentiment Analysis API documentation on dandelion.eu: https://dandelion.eu/docs/api/datatxt/sent/v1/

The Sentiment Analysis API
===========================

The Sentiment API analyses a text and tells whether the expressed opinion is positive,
negative, or neutral. Given a short sentence, it returns a label representing the
identified sentiment, along with a numeric score ranging from stronglypositive (1.0)
to extremely negative (-1.0). It currently works on texts in English and Italian.

First of all you have to authenticate yourself using the ``token`` (or the pair ``app_id`` / ``app_key``)::

    >>> from dandelion import Sentiment
    >>> sentiment = Sentiment(token='')

Then you can take advantage of the Sentiment API::

    >>> results = sentiment.sent('The best film I have ever seen')
    >>> print(results['sentiment'])
    {'score': 0.7, 'type': 'positive'}

NOTE: you can also specify the text language using the ``lang`` parameter (by default the language is
automatically recognized).

Check out the `Sentiment Analysis API documentation on dandelion.eu`_ for more information.