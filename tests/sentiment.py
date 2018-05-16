from __future__ import unicode_literals

import json
import os
from unittest import TestCase

from mock import patch
from requests import sessions

from dandelion import DandelionException, Sentiment
from tests.utils import MockResponse


class TestSentiment(TestCase):
    def setUp(self):
        self.sentiment = Sentiment(token='token')
        f = open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'data.json'))
        self.data = json.load(f, 'utf-8')

    def test_sent_with_unsupported_language(self):
        with self.assertRaises(DandelionException) as context:
            self.sentiment.sent('The worst film I have ever seen', lang='es')

        self.assertEqual(
            context.exception.message, 'Illegal \'lang\' parameter value!'
        )

    def test_sent(self):
        with patch.object(sessions.Session, 'post', return_value=MockResponse(True, self.data['sentiment_test_sent'])) as mock_method:
            res = self.sentiment.sent('The worst film I have ever seen')
            self.assertEqual(
                res.sentiment.type, 'negative'
            )
            self.assertEqual(
                res.sentiment.score, -0.8
            )

        mock_method.assert_called_once_with(
            data={'text': 'The worst film I have ever seen', 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datatxt/sent/v1'
        )

    def test_sent_with_language_parameter(self):
        with patch.object(sessions.Session, 'post', return_value=MockResponse(True, self.data['sentiment_test_sent_with_language_parameter'])) as mock_method:
            res = self.sentiment.sent('worst', lang='en')
            self.assertEqual(
                res.sentiment.type, 'negative'
            )
            self.assertEqual(
                res.sentiment.score, -0.8
            )

        mock_method.assert_called_once_with(
            data={'text': 'worst', 'token': 'token', 'lang': 'en'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datatxt/sent/v1'
        )
