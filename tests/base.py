""" tests can be run from the root dir with:
find -name \*.pyc -delete && coverage run --source=. --branch `which nosetests` tests/*.py tests/cache/*.py  && coverage html
"""
from unittest import TestCase

from mock import patch

from dandelion import (DandelionException, Datagem, DataTXT, Sentiment,
                       default_config)
from dandelion.base import BaseDandelionRequest
from dandelion.utils import AttributeDict


class TestDefaultConfiguration(TestCase):
    TOKEN = 'token'
    APP_ID = 'app_id'
    APP_KEY = 'app_key'

    def tearDown(self):
        # cleanup default config
        for key in ['token', 'app_id', 'app_key']:
            if key in default_config:
                del default_config[key]

    def test_authentication_is_required(self):
        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions')
        self.assertEqual(
            context.exception.message, 'You have to specify the authentication token OR the app_id and app_key!'
        )

        with self.assertRaises(DandelionException) as context:
            DataTXT()
        self.assertEqual(
            context.exception.message, 'You have to specify the authentication token OR the app_id and app_key!'
        )

        with self.assertRaises(DandelionException) as context:
            Sentiment()
        self.assertEqual(
            context.exception.message, 'You have to specify the authentication token OR the app_id and app_key!'
        )

    def test_legacy_authentication_without_app_key(self):
        app_id = self.APP_ID

        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions', app_id=app_id)

        self.assertEqual(
            context.exception.message,
            'To use the legacy authentication system you have to specify both \'app_id\' and \'app_key\'!'
        )

    def test_legacy_authentication_without_app_id(self):
        app_key = self.APP_KEY

        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions', app_key=app_key)

        self.assertEqual(
            context.exception.message,
            'To use the legacy authentication system you have to specify both \'app_id\' and \'app_key\'!'
        )

    def test_can_set_default_config_app_id(self):
        default_config['app_id'] = self.APP_ID

        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions')

        self.assertEqual(
            context.exception.message, 'To use the legacy authentication system you have to specify both \'app_id\' and \'app_key\' (in default config)!'
        )

    def test_can_set_default_config_app_key(self):
        default_config['app_key'] = self.APP_KEY

        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions')

        self.assertEqual(
            context.exception.message, 'To use the legacy authentication system you have to specify both \'app_id\' and \'app_key\' (in default config)!'
        )

    def test_can_authenticate_using_token(self):
        token = self.TOKEN

        Datagem('administrative-regions', token=token)
        DataTXT(token=token)
        Sentiment(token=token)

    def test_can_authenticate_using_app_key_and_id(self):
        app_id = self.APP_ID
        app_key = self.APP_KEY

        Datagem('administrative-regions', app_id=app_id, app_key=app_key)
        DataTXT(app_id=app_id, app_key=app_key)
        Sentiment(app_id=app_id, app_key=app_key)

    def test_can_authenticate_using_default_config_token(self):
        default_config['token'] = self.TOKEN

        Datagem('administrative-regions')
        DataTXT()
        Sentiment()

    def test_can_authenticate_using_default_config_app_id_and_key(self):
        default_config['app_id'] = self.APP_ID
        default_config['app_key'] = self.APP_KEY

        Datagem('administrative-regions')
        DataTXT()
        Sentiment()

    def test_too_many_authentication_params(self):
        token = self.TOKEN
        app_id = self.APP_ID
        app_key = self.APP_KEY

        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions', token=token, app_id=app_id, app_key=app_key)

        self.assertEqual(
            context.exception.message, 'Too many authentication parameters, you have to specify \'token\' OR \'app_id\' and \'app_key\'!'
        )

    def test_too_many_authentication_params_in_default_config(self):
        default_config['token'] = self.TOKEN
        default_config['app_id'] = self.APP_ID

        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions')

        self.assertEqual(
            context.exception.message, 'Too many authentication parameters (in default config), you have to specify \'token\' OR \'app_id\' and \'app_key\'!'
        )

    def test_cannot_set_other_default_config_params(self):
        with self.assertRaises(DandelionException) as context:
            default_config['foo'] = 42

        self.assertEqual(
            context.exception.message, "invalid config param: foo"
        )


class TestAttributeDict(TestCase):
    def test_simple(self):
        obj = AttributeDict()

        obj.name = 'foo'
        self.assertEqual(obj.name, 'foo')

        del obj.name
        with self.assertRaises(KeyError):
            print(obj.name)


class TestBaseClass(TestCase):

    @staticmethod
    def _make_class(require_auth=True, implement_abstract=False):
        class TestClass(BaseDandelionRequest):
            REQUIRE_AUTH = require_auth

            def _get_uri_tokens(self):
                if implement_abstract:
                    return ['']
                return super(TestClass, self)._get_uri_tokens()

        return TestClass

    def test_abstract_methods(self):
        with self.assertRaises(NotImplementedError):
            self._make_class(require_auth=False)()

    def test_authentication_required_with_token(self):
        with self.assertRaises(DandelionException) as context:
            self._make_class(require_auth=True, implement_abstract=True)()

        self.assertEqual(
            context.exception.message, 'You have to specify the authentication token OR the app_id and app_key!'
        )

        obj = self._make_class(require_auth=True, implement_abstract=True)(
            token='tk'
        )
        with patch.object(obj, '_do_raw_request') as _do_raw_request:
            _do_raw_request.return_value.ok = True
            _do_raw_request.return_value.content = '{}'
            obj.do_request(params=dict(foo='bar'))

            _do_raw_request.assert_called_once_with(
                'https://api.dandelion.eu',
                {'foo': 'bar', 'token': 'tk'},
                'post'
            )

    def test_authentication_required_with_app_id_and_key(self):
        with self.assertRaises(DandelionException) as context:
            self._make_class(require_auth=True, implement_abstract=True)()

        self.assertEqual(
            context.exception.message, 'You have to specify the authentication token OR the app_id and app_key!'
        )

        obj = self._make_class(require_auth=True, implement_abstract=True)(
            app_id='aa', app_key='bb'
        )
        with patch.object(obj, '_do_raw_request') as _do_raw_request:
            _do_raw_request.return_value.ok = True
            _do_raw_request.return_value.content = '{}'
            obj.do_request(params=dict(foo='bar'))

            _do_raw_request.assert_called_once_with(
                'https://api.dandelion.eu',
                {'foo': 'bar', '$app_id': 'aa', '$app_key': 'bb'},
                'post'
            )

    def test_authentication_not_required(self):
        obj = self._make_class(require_auth=False, implement_abstract=True)()
        with patch.object(obj, '_do_raw_request') as _do_raw_request:
            _do_raw_request.return_value.ok = True
            _do_raw_request.return_value.content = '{}'
            obj.do_request(params=dict(foo='bar'))

            _do_raw_request.assert_called_once_with(
                'https://api.dandelion.eu', dict(foo='bar'), 'post'
            )
