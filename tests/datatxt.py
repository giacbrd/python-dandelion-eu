from __future__ import unicode_literals

import os
from unittest import TestCase

from dandelion import DataTXT, default_config, DandelionException


class TestDatatxt(TestCase):
    def setUp(self):
        default_config['app_id'] = os.environ['APP_ID']
        default_config['app_key'] = os.environ['APP_KEY']
        self.datatxt = DataTXT()

    def test_nex(self):
        res = self.datatxt.nex('They say Apple is better than Windows')
        self.assertEqual(
            {annotation.uri for annotation in res.annotations},
            {'http://en.wikipedia.org/wiki/Apple_Inc.',
             'http://en.wikipedia.org/wiki/Microsoft_Windows'}
        )

    def test_sim(self):
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

    def test_li(self):
        res = self.datatxt.li("Le nostre tre M sono: mafia, mamma, mandolino")

        self.assertEqual(
            [entry.lang for entry in res.detectedLangs],
            ['it']
        )

        self.assertGreater(res.detectedLangs[0].confidence, 0.9999)

    def test_raises_on_error(self):
        with self.assertRaises(DandelionException):
            self.datatxt.nex(text=None)

    def test_can_set_host(self):
        self.datatxt = DataTXT(host="api.dandelion.eu")
        self.test_nex()

        self.datatxt = DataTXT(host="http://api.dandelion.eu")
        self.test_nex()
