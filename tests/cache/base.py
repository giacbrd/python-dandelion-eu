import json

from mock import MagicMock
from unittest import TestCase

from dandelion.base import BaseDandelionRequest
from dandelion.cache import NoCache


class FakeResponse(object):
    def __init__(self, ok=True, content='{}'):
        self.ok = True
        self.content = content


class FakeDandelionRequest(BaseDandelionRequest):
    REQUIRE_AUTH = False
    last_cache_status = None

    def method1(self, **params):
        return self.do_request(params, ('method1', ))

    def method2(self, **params):
        return self.do_request(params, ('method2', ))

    def do_request(self, *args, **kwargs):
        self.last_cache_status = 'hit'
        return super(FakeDandelionRequest, self).do_request(
            *args, **kwargs
        )

    def _do_raw_request(self, url, params, **kwargs):
        self.last_cache_status = 'miss'
        return FakeResponse(ok=True, content=json.dumps(
            dict(url=url, params=params)
        ))

    def _get_uri_tokens(self):
        return []


class CacheBaseMixin(object):
    req_obj = None

    def test_simple(self):
        resp = self.req_obj.method1()
        self.assertEqual(self.req_obj.last_cache_status, 'miss')
        self.assertEqual(
            resp, {'url': 'https://api.dandelion.eu/method1', 'params': {}}
        )

        resp = self.req_obj.method1()
        self.assertEqual(self.req_obj.last_cache_status, 'hit')
        self.assertEqual(
            resp, {'url': 'https://api.dandelion.eu/method1', 'params': {}}
        )

        resp = self.req_obj.method1(param1='1', param2='2')
        self.assertEqual(self.req_obj.last_cache_status, 'miss')
        self.assertEqual(
            resp, {'url': 'https://api.dandelion.eu/method1', 'params': {
                'param1': '1',
                'param2': '2',
            }}
        )

        resp = self.req_obj.method1(param1='1', param2='2')
        self.assertEqual(self.req_obj.last_cache_status, 'hit')
        self.assertEqual(
            resp, {'url': 'https://api.dandelion.eu/method1', 'params': {
                'param1': '1',
                'param2': '2',
            }}
        )

        resp = self.req_obj.method1(param2='2', param1='1')
        self.assertEqual(self.req_obj.last_cache_status, 'hit')
        self.assertEqual(
            resp, {'url': 'https://api.dandelion.eu/method1', 'params': {
                'param1': '1',
                'param2': '2',
            }}
        )

        resp = self.req_obj.method1(foo='bar')
        self.assertEqual(self.req_obj.last_cache_status, 'miss')
        self.assertEqual(
            resp, {'url': 'https://api.dandelion.eu/method1', 'params': {
                'foo': 'bar',
            }}
        )

        resp = self.req_obj.method2(foo='bar')
        self.assertEqual(self.req_obj.last_cache_status, 'miss')
        self.assertEqual(
            resp, {'url': 'https://api.dandelion.eu/method2', 'params': {
                'foo': 'bar',
            }}
        )

        resp = self.req_obj.method2(foo='bar')
        self.assertEqual(self.req_obj.last_cache_status, 'hit')
        self.assertEqual(
            resp, {'url': 'https://api.dandelion.eu/method2', 'params': {
                'foo': 'bar',
            }}
        )

        resp = self.req_obj.method1(foo='bar')
        self.assertEqual(self.req_obj.last_cache_status, 'hit')
        self.assertEqual(
            resp, {'url': 'https://api.dandelion.eu/method1', 'params': {
                'foo': 'bar',
            }}
        )


class TestNoCache(CacheBaseMixin, TestCase):

    def setUp(self):
        self.req_obj = FakeDandelionRequest(cache=NoCache())

    def test_simple(self):
        for _ in range(3):
            resp = self.req_obj.method1()
            self.assertEqual(self.req_obj.last_cache_status, 'miss')
            self.assertEqual(
                resp, {'url': 'https://api.dandelion.eu/method1', 'params': {}}
            )

    def test_get_raises_exception(self):
        with self.assertRaises(NotImplementedError):
            self.req_obj.cache.get('key')
