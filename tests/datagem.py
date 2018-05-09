from __future__ import unicode_literals

import os
import warnings
from datetime import datetime
from unittest import TestCase

from dandelion import DandelionException, Datagem, default_config
from dandelion.datagem import DatagemManager


class TestDatagemBase(TestCase):
    def setUp(self):
        default_config['app_id'] = os.environ['APP_ID']
        default_config['app_key'] = os.environ['APP_KEY']
        self.datagem = Datagem('administrative-regions')

    @staticmethod
    def _achene(achene_id):
        return 'http://dandelion.eu/resource/{}'.format(achene_id)


class TestDatagem(TestDatagemBase):
    def test_select(self):
        for item in self.datagem.items.select('name').where(
            acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
        ):
            self.assertEqual(item, dict(name='Trento'))

    def test_select_multiple(self):
        for item in self.datagem.items.select('name', 'population').where(
            acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
        ):
            self.assertEqual(
                item, dict(name='Trento', population={"2001": None, "2011": 114063})
            )

    def test_select_concat(self):
        items = self.datagem.items.select('name')
        for item in items.select('population').where(
            acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
        ):
            self.assertEqual(
                item, dict(population={"2001": None, "2011": 114063})
            )

    def test_select_empty(self):
        self.assertEqual(
            list(self.datagem.items.select()[:1]),
            list(self.datagem.items[:1])
        )

    def test_group(self):
        items = self.datagem.items.select('name', 'level', 'count()')
        items = items.where(name='Trento')
        self.assertEqual(sorted(items, key=lambda x: x['level']), [
            dict(name='Trento', level=50, count_1=1),
            dict(name='Trento', level=60, count_1=1),
            dict(name='Trento', level=70, count_1=3),
        ])

    def test_where(self):
        for item in self.datagem.items.where(parentNames__municipality='Ala'):
            self.assertEqual(
                item['parentNames']['municipality'], 'Ala'
            )

    def test_where_empty(self):
        self.assertEqual(
            list(self.datagem.items.select('acheneID').where()[:5]),
            list(self.datagem.items.select('acheneID')[:5])
        )

    def test_where_multiple(self):
        for item in self.datagem.items.where(name='Trento', level=60):
            self.assertEqual(item['name'], 'Trento')
            self.assertEqual(item['level'], 60)

    def test_where_concat(self):
        for item in self.datagem.items.where(name='Trento').where(level=60):
            self.assertEqual(item['name'], 'Trento')
            self.assertEqual(item['level'], 60)

    def test_where_greater_then_equal(self):
        items = self.datagem.items.select('population')
        items = items.order('population.2011')
        items = list(items.where(population__2011__gte=114063)[:50])
        self.assertTrue(
            all(x['population']['2011'] >= 114063 for x in items)
        )
        self.assertTrue(
            any(x['population']['2011'] == 114063 for x in items)
        )

    def test_where_greater_then(self):
        items = self.datagem.items.select('population')
        items = items.order('population.2011')
        items = list(items.where(population__2011__gt=114063)[:50])
        self.assertTrue(
            all(x['population']['2011'] >= 114063 for x in items)
        )
        self.assertFalse(
            any(x['population']['2011'] == 114063 for x in items)
        )

    def test_where_lower_then_equal(self):
        items = self.datagem.items.select('population')
        items = items.order('population.2011 DESC')
        items = list(items.where(population__2011__lte=114063)[:50])
        self.assertTrue(
            all(x['population']['2011'] <= 114063 for x in items)
        )
        self.assertTrue(
            any(x['population']['2011'] == 114063 for x in items)
        )

    def test_where_lower_then(self):
        items = self.datagem.items.select('population')
        items = items.order('population.2011 DESC')
        items = list(items.where(population__2011__lt=114063)[:50])
        self.assertTrue(
            all(x['population']['2011'] <= 114063 for x in items)
        )
        self.assertFalse(
            any(x['population']['2011'] == 114063 for x in items)
        )

    def test_where_not(self):
        items = self.datagem.items.select('population')
        items = items.order('population.2011 DESC')
        items = items.where(population__2011__gte=110000)
        items = list(items.where(population__2011__not=114063)[:50])
        self.assertTrue(
            all(x['population']['2011'] != 114063 for x in items)
        )
        self.assertTrue(
            any(x['population']['2011'] > 114063 for x in items)
        )
        self.assertTrue(
            any(x['population']['2011'] < 114063 for x in items)
        )

    def test_get(self):
        item = self.datagem.items.select('name').get(
            acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
        )
        self.assertEqual(item, dict(name='Trento'))

    def test_get_item(self):
        item = self.datagem.items.select('name').where(
            acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
        )[0]
        self.assertEqual(item, dict(name='Trento'))

    def test_get_with_no_result(self):
        with self.assertRaises(DandelionException) as context:
            self.datagem.items.select('name').get(
                acheneID=self._achene('42')
            )
        self.assertEqual(
            context.exception.message, 'The requested item does not exist'
        )

    def test_order(self):
        items = self.datagem.items.select('population')
        items = items.order('population.2011')[:5]

        pops = [x['population']['2011'] for x in items]
        self.assertEqual(pops, sorted(pops))

    def test_order_desc(self):
        items = self.datagem.items.select('population')
        items = items.where(population__2011__not=None)
        items = items.order('population.2011 DESC')[:5]

        pops = [x['population']['2011'] for x in items]
        self.assertEqual(pops, sorted(pops, reverse=True))

    def test_limit(self):
        objects = list(self.datagem.items[:5])
        self.assertEqual(len(objects), 5)

    def test_offset(self):
        first_half = list(self.datagem.items[:5])
        second_half = list(self.datagem.items[5:10])
        full_list = list(self.datagem.items[:10])
        self.assertEqual(first_half + second_half, full_list)

    def test_pagination(self):
        page_size = DatagemManager.PAGINATE_BY
        items = list(self.datagem.items.select('acheneID')[:page_size + 10])
        self.assertEqual(len(items), page_size + 10)
        self.assertEqual(
            # check pagination does not return the same item twice
            len(items), len(frozenset(x['acheneID'] for x in items))
        )

    def test_step(self):
        items = list(self.datagem.items.select('acheneID')[:5])
        some_items = list(self.datagem.items.select('acheneID')[:5:2])
        self.assertEqual(some_items, items[::2])

    def test_invalid_slice(self):
        for the_slice in ['key', [], {}]:
            with self.assertRaises(TypeError) as context:
                list(self.datagem.items[the_slice])
            self.assertEqual(
                str(context.exception),
                "Invalid slice type: {}".format(type(the_slice))
            )

        for the_slice in [slice(-1), slice(0, -1), slice(-1, None)]:
            with self.assertRaises(TypeError) as context:
                list(self.datagem.items[the_slice])
            self.assertEqual(
                str(context.exception),
                'Negative indexes are not supported'
            )

        for the_slice in [slice(0, None, -1), slice(0, None, 0)]:
            with self.assertRaises(TypeError) as context:
                list(self.datagem.items[the_slice])
            self.assertEqual(
                str(context.exception),
                'Non-positive step is not supported'
            )

    def test_negative_index(self):
        with self.assertRaises(TypeError) as context:
            list(self.datagem.items[-1])

        self.assertEqual(
            str(context.exception),
            "Negative indexes are not supported"
        )

    def test_version(self):
        now = datetime.now()
        self.assertIsNotNone(self.datagem.version)
        self.assertGreater((datetime.now() - now).total_seconds(), 0.3)
        self.assertLess((datetime.now() - now).total_seconds(), 1.0)

        now = datetime.now()
        self.assertEqual(len(self.datagem.version), 40)
        self.assertLess((datetime.now() - now).total_seconds(), 0.01)


class TestDeprecatedCode(TestDatagemBase):
    def test_objects(self):
        with warnings.catch_warnings(record=True) as warn:
            warnings.simplefilter("always")

            items = list(self.datagem.objects.select('acheneID')[:5])

            # Verify some things
            self.assertEqual(len(items), 5)
            self.assertEqual(len(warn), 1)
            self.assertEqual(warn[0].category, DeprecationWarning)
            self.assertEqual(
                '"objects" is deprecated, use "items" instead',
                str(warn[0].message)
            )
