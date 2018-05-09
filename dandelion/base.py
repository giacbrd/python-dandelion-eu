""" base classes
"""
from __future__ import unicode_literals

import requests

from dandelion.cache.base import NoCache
from dandelion.utils import AttributeDict

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse


class DandelionConfig(dict):
    """ class for storing the default dandelion configuration, such
     as authentication parameters
    """
    ALLOWED_KEYS = ['token', 'app_id', 'app_key']

    def __setitem__(self, key, value):
        if key not in self.ALLOWED_KEYS:
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
    def __init__(self, mode):
        super(MissingParameterException, self).__init__(
            'To use the legacy authentication system you have to specify both \'app_id\' and \'app_key\''+mode+'!'
        )


class TooManyParametersException(DandelionException):
    def __init__(self, mode):
        super(TooManyParametersException, self).__init__(
            'Too many authentication parameters'+mode+', you have to specify \'token\' OR \'app_id\' and \'app_key\'!'
        )


class BaseDandelionRequest(object):
    DANDELION_HOST = 'api.dandelion.eu'
    REQUIRE_AUTH = True

    def __init__(self, host=None, cache=NoCache(), token=None, app_id=None, app_key=None, **kwargs):
        from dandelion import default_config
        self.uri = self._get_uri(host=host)
        self.requests = requests.session()
        self.cache = cache

        if self.REQUIRE_AUTH:
            self.auth = ''

            if not self._check_authentication_parameters(token, app_id, app_key, ''):
                token = default_config.get('token')
                app_id = default_config.get('app_id')
                app_key = default_config.get('app_key')

                if not self._check_authentication_parameters(token, app_id, app_key, ' (in default config)'):
                    raise DandelionException('You have to specify the authentication token OR the app_id and app_key!')

    def _check_authentication_parameters(self, token, app_id, app_key, mode):
        if token:
            if not app_id and not app_key:
                self.auth = 'token'
                self.token = token
                return True
            else:
                raise TooManyParametersException(mode)
        else:
            if app_id and app_key:
                self.auth = 'legacy'
                self.app_id = app_id
                self.app_key = app_key
                return True
            elif app_id or app_key:
                raise MissingParameterException(mode)
        return False

    def do_request(self, params, extra_url='', method='post', **kwargs):
        if self.REQUIRE_AUTH:
            if self.auth == 'token':
                params['token'] = self.token
            elif self.auth == 'legacy':
                params['$app_id'] = self.app_id
                params['$app_key'] = self.app_key
            else:
                raise DandelionException('Error in authentication mechanism!')

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
