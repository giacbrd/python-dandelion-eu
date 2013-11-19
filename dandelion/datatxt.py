""" classes for querying the dataTXT family
"""
from dandelion.base import BaseDandelionRequest


class DataTXT(BaseDandelionRequest):
    """ class for accessing the dataTXT family
    """
    def nex(self, text, **params):
        return self.do_get(
            dict(params, text=text), ('nex', 'v1')
        )

    def sim(self, text1, text2, **params):
        return self.do_get(
            dict(params, text1=text1, text2=text2), ('sim', 'v1')
        )

    def li(self, text, **params):
        return self.do_get(
            dict(params, text=text), ('li', 'v1')
        )

    def _get_uri_tokens(self):
        return 'datatxt',
