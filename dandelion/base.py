""" base classes
"""
from __future__ import unicode_literals
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

import json
import requests

from dandelion.cache.base import NoCache
from dandelion.utils import AttributeDict


class DandelionConfig(dict):
    """ class for storing the default dandelion configuration, such
     as authentication parameters
    """
    ALLOWED_KEYS = ['app_id', 'app_key']

    def __setitem__(self, key, value):
        if not key in self.ALLOWED_KEYS:
            raise DandelionException('invalid config param: {}'.format(key))
        super(DandelionConfig, self).__setitem__(key, value)


class DandelionException(BaseException):
    error = True

    def __init__(self, dandelion_obj=None, **kwargs):
        if isinstance(dandelion_obj, AttributeDict):
            self.message = dandelion_obj.message
            self.code = dandelion_obj.code
            self.data = dandelion_obj.data
        else:
            self.message = "{}".format(dandelion_obj)
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
        from dandelion import default_config
        self.uri = self._get_uri(host=kwargs.get('host'))
        self.app_id = kwargs.get('app_id', default_config.get('app_id'))
        self.app_key = kwargs.get('app_key', default_config.get('app_key'))
        self.requests = requests.session()
        self.cache = kwargs.get('cache', NoCache())

        if self.REQUIRE_AUTH and not self.app_id:
            raise MissingParameterException("app_id")
        if self.REQUIRE_AUTH and not self.app_key:
            raise MissingParameterException("app_key")

    def do_request(self, params, extra_url='', **kwargs):
        if self.REQUIRE_AUTH:
            params['$app_id'] = self.app_id
            params['$app_key'] = self.app_key

        url = self.uri + ''.join('/' + x for x in extra_url)

        cache_key = self.cache.get_key_for(
            url=url, params=params,
        )

        if self.cache.contains_key(cache_key):
            response = self.cache.get(cache_key)
        else:
            response = self._do_raw_request(url, params, **kwargs)
            if response.ok:
                self.cache.set(cache_key, response)

        obj = response.json(object_hook=AttributeDict)
        if not response.ok:
            raise DandelionException(obj)
        return obj

    def _get_uri(self, host=None):
        base_uri = host or self.DANDELION_HOST
        if not base_uri.startswith('http'):
            base_uri = 'https://' + base_uri
        return urlparse.urljoin(
            base_uri, '/'.join(self._get_uri_tokens())
        )

    def _do_raw_request(self, url, params, **kwargs):
        return self.requests.post(
            url=url, data=params, **kwargs
        )

    def _get_uri_tokens(self):
        raise NotImplementedError
