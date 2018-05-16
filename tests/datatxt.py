from __future__ import unicode_literals

import json
import os
from unittest import TestCase

from mock import patch
from requests import sessions

from dandelion import DandelionException, DataTXT
from tests.utils import MockResponse


class TestDatatxt(TestCase):
    def setUp(self):
        self.datatxt = DataTXT(token='token')
        f = open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'data.json'))
        self.data = json.load(f, 'utf-8')

    def test_nex_with_not_integer_top_entities(self):
        with self.assertRaises(DandelionException) as context:
            self.datatxt.nex('They say Apple is better than Windows', top_entities='a')

        self.assertEqual(
            context.exception.message, 'The \'top-entities\' parameter must be an integer greater than or equal to 0'
        )

    def test_nex_with_top_entities_illegal_value(self):
        with self.assertRaises(DandelionException) as context:
            self.datatxt.nex('They say Apple is better than Windows', top_entities=-8)

        self.assertEqual(
            context.exception.message, 'The \'top-entities\' parameter must be an integer greater than or equal to 0'
        )

    def test_nex_with_not_float_min_confidence(self):
        with self.assertRaises(DandelionException) as context:
            self.datatxt.nex('They say Apple is better than Windows', min_confidence='b')

        self.assertEqual(
            context.exception.message, 'The \'top-entities\' parameter must be a float between 0.0 and 1.0'
        )

    def test_nex_with_min_confidence_illegal_values(self):
        with self.assertRaises(DandelionException) as context:
            self.datatxt.nex('They say Apple is better than Windows', min_confidence=-0.5)

        self.assertEqual(
            context.exception.message, 'The \'top-entities\' parameter must be a float between 0.0 and 1.0'
        )

        with self.assertRaises(DandelionException) as context:
            self.datatxt.nex('They say Apple is better than Windows', min_confidence=4.3)

        self.assertEqual(
            context.exception.message, 'The \'top-entities\' parameter must be a float between 0.0 and 1.0'
        )

    def test_nex(self):
        with patch.object(sessions.Session, 'post', return_value=MockResponse(True, self.data['datatxt_test_nex'])) as mock_method:
            res = self.datatxt.nex('They say Apple is better than Windows')
            self.assertEqual(
                {annotation.uri for annotation in res.annotations},
                {'http://en.wikipedia.org/wiki/Apple_Inc.',
                 'http://en.wikipedia.org/wiki/Microsoft_Windows'}
            )

        mock_method.assert_called_once_with(
            data={'text': 'They say Apple is better than Windows', 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datatxt/nex/v1'
        )

    def test_nex_with_min_confidence(self):
        with patch.object(sessions.Session, 'post', return_value=MockResponse(True, self.data['datatxt_test_nex_with_min_confidence'])) as mock_method:
            res = self.datatxt.nex('They say Apple is better than Windows', min_confidence=0.7)
            self.assertEqual(
                len(res.annotations), 1
            )
            self.assertEqual(
                res.annotations[0].confidence, 0.735
            )
            self.assertEqual(
                res.annotations[0].uri, 'http://en.wikipedia.org/wiki/Apple_Inc.'
            )

        mock_method.assert_called_once_with(
            data={'text': 'They say Apple is better than Windows', 'token': 'token', 'min_confidence': 0.7},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datatxt/nex/v1'
        )

    def test_nex_top_entities(self):
        with patch.object(sessions.Session, 'post', return_value=MockResponse(True, self.data['datatxt_test_nex_top_entities'])) as mock_method:
            res = self.datatxt.nex('They say Apple is better than Windows', top_entities=1)
            self.assertEqual(
                len(res.topEntities), 1
            )
            self.assertEqual(
                res.topEntities[0].score, 0.3768116
            )
            self.assertEqual(
                res.topEntities[0].uri, 'http://en.wikipedia.org/wiki/Apple_Inc.'
            )

        mock_method.assert_called_once_with(
            data={'text': 'They say Apple is better than Windows', 'token': 'token', 'top_entities': 1},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datatxt/nex/v1'
        )

    def test_sim(self):
        with patch.object(sessions.Session, 'post', return_value=MockResponse(True, self.data['datatxt_test_sim'])) as mock_method:
            res = self.datatxt.sim(
                'Reports that the NSA eavesdropped on world leaders have "severely'
                ' shaken" relations between Europe and the U.S., German Chancellor'
                ' Angela Merkel said.',
                # --
                'Germany and France are to seek talks with the US to settle a row '
                'over spying, as espionage claims continue to overshadow an EU '
                'summit in Brussels.'
            )
            self.assertGreater(res.similarity, 0.5)

        mock_method.assert_called_once_with(
            data={'text1': 'Reports that the NSA eavesdropped on world leaders have "severely shaken" relations between Europe and the U.S., German Chancellor Angela Merkel said.', 'text2': 'Germany and France are to seek talks with the US to settle a row over spying, as espionage claims continue to overshadow an EU summit in Brussels.', 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datatxt/sim/v1'
        )

    def test_li(self):
        with patch.object(sessions.Session, 'post', return_value=MockResponse(True, self.data['datatxt_test_li'])) as mock_method:
            res = self.datatxt.li('Le nostre tre M sono: mafia, mamma, mandolino')
            self.assertEqual(
                [entry.lang for entry in res.detectedLangs],
                ['it']
            )
            self.assertGreater(res.detectedLangs[0].confidence, 0.9999)

        mock_method.assert_called_once_with(
            data={
                'text': 'Le nostre tre M sono: mafia, mamma, mandolino',
                'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datatxt/li/v1'
        )

    def test_raises_on_error(self):
        with self.assertRaises(DandelionException):
            self.datatxt.nex(text=None)

    def test_can_set_host(self):
        self.datatxt = DataTXT(host="api.dandelion.eu", token='token')

        with patch.object(sessions.Session, 'post', return_value=MockResponse(True, self.data['datatxt_test_can_set_host_1'])) as mock_method:
            res = self.datatxt.nex('They say Apple is better than Windows')
            self.assertEqual(
                {annotation.uri for annotation in res.annotations},
                {'http://en.wikipedia.org/wiki/Apple_Inc.',
                 'http://en.wikipedia.org/wiki/Microsoft_Windows'}
            )

        mock_method.assert_called_once_with(
            data={'text': 'They say Apple is better than Windows', 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datatxt/nex/v1'
        )

        self.datatxt = DataTXT(host="http://api.dandelion.eu", token='token')
        with patch.object(sessions.Session, 'post', return_value=MockResponse(True, self.data['datatxt_test_can_set_host_2'])) as mock_method:
            res = self.datatxt.nex('They say Apple is better than Windows')
            self.assertEqual(
                {annotation.uri for annotation in res.annotations},
                {'http://en.wikipedia.org/wiki/Apple_Inc.',
                 'http://en.wikipedia.org/wiki/Microsoft_Windows'}
            )

        mock_method.assert_called_once_with(
            data={'text': 'They say Apple is better than Windows', 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='http://api.dandelion.eu/datatxt/nex/v1'
        )
