""" classes for querying the Sentiment API
"""
from dandelion.base import BaseDandelionRequest, DandelionException


class Sentiment(BaseDandelionRequest):
    """ class for accessing the Sentiment API
        """
    def sent(self, text, lang=None, **params):
        if lang is not None and lang not in ['en', 'it', 'auto']:
            raise DandelionException('Illegal \'lang\' parameter value!')

        return self.do_request(
            dict(params, text=text, lang=lang), ('sent', 'v1')
        )

    def _get_uri_tokens(self):
        return 'datatxt',
