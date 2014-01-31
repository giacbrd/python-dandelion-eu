""" tests can be run from the root dir with:
APP_ID={} APP_KEY={} coverage run --source=. --branch nosetests tests/*
"""
import os

from unittest import TestCase
from dandelion import Datagem, DandelionException, DataTXT, default_config


class TestDefaultConfiguration(TestCase):
    def tearDown(self):
        # cleanup default config
        for key in ['app_id', 'app_key']:
            if key in default_config:
                del default_config[key]

    def test_can_set_app_id(self):
        default_config['app_id'] = os.environ['APP_ID']

        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions')

        self.assertEqual(
            context.exception.message, 'Param "app_key" is required'
        )

    def test_can_set_app_key(self):
        default_config['app_key'] = os.environ['APP_KEY']

        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions')

        self.assertEqual(
            context.exception.message, 'Param "app_id" is required'
        )

    def test_can_authenticate(self):
        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions')
        self.assertEqual(
            context.exception.message, 'Param "app_id" is required'
        )

        with self.assertRaises(DandelionException) as context:
            DataTXT()
        self.assertEqual(
            context.exception.message, 'Param "app_id" is required'
        )

        default_config['app_id'] = os.environ['APP_ID']
        default_config['app_key'] = os.environ['APP_KEY']

        Datagem('administrative-regions')
        DataTXT()

    def test_cannot_set_other_params(self):
        with self.assertRaises(DandelionException) as context:
            default_config['foo'] = 42

        self.assertEqual(
            context.exception.message, "invalid config param: foo"
        )
