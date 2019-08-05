""" classes for querying the dataTXT family
"""
from dandelion.base import BaseDandelionRequest


class DataTXT(BaseDandelionRequest):
    """ class for accessing the dataTXT family
    """
    def nex(self, text='', **params):
        if 'min_confidence' not in params:
            params['min_confidence'] = 0.6
        if text:
            params['text'] = text
        return self.do_request(
            params, ('nex', 'v1')
        )

    def sim(self, text1='', text2='', **params):
        if text1:
            params['text1'] = text1
        if text2:
            params['text2'] = text2
        return self.do_request(
            params, ('sim', 'v1')
        )

    def li(self, text='', **params):
        if text:
            params['text'] = text
        return self.do_request(
            params, ('li', 'v1')
        )

    def _get_uri_tokens(self):
        return 'datatxt',
