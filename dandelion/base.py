""" base classes
"""
import json
import urlparse

import requests

from dandelion.utils import AttributeDict


class DandelionException(BaseException):
    error = True

    def __init__(self, dandelion_obj=None, **kwargs):
        if isinstance(dandelion_obj, AttributeDict):
            self.message = dandelion_obj.message
            self.code = dandelion_obj.code
            self.data = dandelion_obj.data
        elif isinstance(dandelion_obj, basestring):
            self.message = dandelion_obj
        else:
            self.message = kwargs.get('message')
            self.code = kwargs.get('code')
            self.data = kwargs.get('data')
        super(DandelionException, self).__init__(self.message)


class MissingParameterException(DandelionException):
    code = 'error.missingParameter'

    def __init__(self, param_name):
        self.data = {'parameter': param_name}
        super(MissingParameterException, self).__init__(
            'Param "{}" is required'.format(param_name)
        )


class BaseDandelionRequest(object):
    DANDELION_HOST = 'api.dandelion.eu'
    REQUIRE_AUTH = True

    def __init__(self, **kwargs):
        self.uri = self._get_uri(host=kwargs.get('host'))
        self.app_id = kwargs.get('app_id')
        self.app_key = kwargs.get('app_key')

        if self.REQUIRE_AUTH and not self.app_id:
            raise MissingParameterException("app_id")
        if self.REQUIRE_AUTH and not self.app_key:
            raise MissingParameterException("app_key")

    def do_get(self, params, extra_url=''):
        if self.REQUIRE_AUTH:
            params['$app_id'] = self.app_id
            params['$app_key'] = self.app_key

        response = requests.get(
            url=self.uri + ''.join('/' + x for x in extra_url),
            params=params,
            verify=False,
        )

        obj = json.loads(response.content, object_hook=AttributeDict)
        if not response.ok:
            raise DandelionException(obj)
        return obj

    def _get_uri(self, host=None):
        base_uri = 'https://' + (host or self.DANDELION_HOST)
        return urlparse.urljoin(
            base_uri, '/'.join(self._get_uri_tokens())
        )

    def _get_uri_tokens(self):
        raise NotImplementedError
