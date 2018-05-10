""" classes for querying the dataTXT family
"""
from dandelion.base import BaseDandelionRequest
from dandelion.base import DandelionException


class DataTXT(BaseDandelionRequest):
    """ class for accessing the dataTXT family
    """
    def nex(self, text, top_entities=None, min_confidence=None, **params):
        if top_entities is not None and (not isinstance(top_entities, (int, long)) or top_entities < 0):
            raise DandelionException('The \'top-entities\' parameter must be an integer greater than or equal to 0')

        if min_confidence is not None and (not isinstance(min_confidence,float) or min_confidence < 0.0 or min_confidence > 1.0):
            raise DandelionException('The \'top-entities\' parameter must be a float between 0.0 and 1.0')

        return self.do_request(
            dict(params, text=text, top_entities=top_entities, min_confidence=min_confidence), ('nex', 'v1')
        )

    def sim(self, text1, text2, **params):
        return self.do_request(
            dict(params, text1=text1, text2=text2), ('sim', 'v1')
        )

    def li(self, text, **params):
        return self.do_request(
            dict(params, text=text), ('li', 'v1')
        )

    def _get_uri_tokens(self):
        return 'datatxt',
