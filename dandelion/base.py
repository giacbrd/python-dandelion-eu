""" base classes
"""
from __future__ import unicode_literals
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

from dandelion.cache.base import NoCache
from dandelion.utils import AttributeDict


class DandelionConfig(dict):
    """ class for storing the default dandelion configuration, such
     as authentication parameters
    """
    ALLOWED_KEYS = ['token',]

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
        import requests
        from dandelion import default_config
        self.uri = self._get_uri(host=kwargs.get('host'))
        self.token = kwargs.get('token', default_config.get('token'))
        self.requests = requests.session()
        self.cache = kwargs.get('cache', NoCache())

        if self.REQUIRE_AUTH and not self.token:
            raise MissingParameterException("token")

    def do_request(self, params, extra_url='', method='post', **kwargs):
        if self.REQUIRE_AUTH:
            params['token'] = self.token

        url = self.uri + ''.join('/' + x for x in extra_url)

        cache_key = self.cache.get_key_for(
            url=url, params=params, method=method
        )

        if self.cache.contains_key(cache_key):
            response = self.cache.get(cache_key)
        else:
            response = self._do_raw_request(url, params, method, **kwargs)
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

    def _do_raw_request(self, url, params, method, **kwargs):
        from dandelion import __version__
        kwargs['data' if method in ('post', 'put') else 'params'] = params
        kwargs['url'] = url
        kwargs['headers'] = kwargs.pop('headers', {})
        kwargs['headers']['User-Agent'] = kwargs['headers'].get(
            'User-Agent', 'python-dandelion-eu/' + __version__
        )
        return getattr(self.requests, method)(**kwargs)

    def _get_uri_tokens(self):
        raise NotImplementedError
