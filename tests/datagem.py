from __future__ import unicode_literals

import json
import os
import warnings
from unittest import TestCase

from mock import call, patch
from requests import sessions

from dandelion import DandelionException, Datagem
from dandelion.datagem import DatagemManager
from tests.utils import MockResponse


class TestDatagemBase(TestCase):
    def setUp(self):
        self.datagem = Datagem('administrative-regions', token='token')
        f = open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'data.json'))
        self.data = json.load(f, 'utf-8')

    @staticmethod
    def _achene(achene_id):
        return 'http://dandelion.eu/resource/{}'.format(achene_id)


class TestDatagem(TestDatagemBase):
    def test_select(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_select'])) as mock_method:
            for item in self.datagem.items.select('name').where(
                    acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
            ):
                self.assertEqual(item, dict(name='Trento'))

        mock_method.assert_called_once_with(
            params={'$select': 'name', '$where': 'acheneID = "http://dandelion.eu/resource/05a192433bede90cd0f12652b1a12c428cb253d5"', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_select_multiple(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_select_multiple'])) as mock_method:
            for item in self.datagem.items.select('name', 'population').where(
                    acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
            ):
                self.assertEqual(
                    item, dict(name='Trento', population={"2001": None, "2011": 114063})
                )

        mock_method.assert_called_once_with(
            params={'$select': 'name,population', '$where': 'acheneID = "http://dandelion.eu/resource/05a192433bede90cd0f12652b1a12c428cb253d5"', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_select_concat(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_select_concat'])) as mock_method:
            items = self.datagem.items.select('name')
            for item in items.select('population').where(
                    acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
            ):
                self.assertEqual(
                    item, dict(name='Trento', population={"2001": None, "2011": 114063})
                )

        mock_method.assert_called_once_with(
            params={'$select': 'name,population', '$where': 'acheneID = "http://dandelion.eu/resource/05a192433bede90cd0f12652b1a12c428cb253d5"', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_select_empty(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_select_empty'])) as mock_method:
            self.assertEqual(
                list(self.datagem.items.select()[:1]),
                list(self.datagem.items[:1])
            )

        expected_arguments = [call(
            params={'$select': '', '$offset': 0, '$limit': 1, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        ), call(
            params={'$offset': 0, '$limit': 1, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )]
        self.assertEqual(mock_method.call_args_list, expected_arguments)

    def test_group(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_group'])) as mock_method:
            items = self.datagem.items.select('name', 'level', 'count()')
            items = items.where(name='Trento')
            self.assertEqual(sorted(items, key=lambda x: x['level']), [
                dict(name='Trento', level=50, count_1=1),
                dict(name='Trento', level=60, count_1=1),
                dict(name='Trento', level=70, count_1=3),
            ])

        mock_method.assert_called_once_with(
            params={'$select': 'name,level,count()', '$group': 'name,level', '$where': 'name = "Trento"', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_where(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_where'])) as mock_method:
            for item in self.datagem.items.where(parentNames__municipality='Ala'):
                self.assertEqual(
                    item['parentNames']['municipality'], 'Ala'
                )

        mock_method.assert_called_once_with(
            params={'$where': 'parentNames.municipality = "Ala"', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_where_empty(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_where_empty'])) as mock_method:
            self.assertEqual(
                list(self.datagem.items.select('acheneID').where()[:5]),
                list(self.datagem.items.select('acheneID')[:5])
            )

        expected_arguments = [call(
            params={'$select': 'acheneID', '$offset': 0, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        ), call(
            params={'$select': 'acheneID', '$offset': 0, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )]
        self.assertEqual(mock_method.call_args_list, expected_arguments)

    def test_where_multiple(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_where_multiple'])) as mock_method:
            for item in self.datagem.items.where(name='Trento', level=60):
                self.assertEqual(item['name'], 'Trento')
                self.assertEqual(item['level'], 60)

        mock_method.assert_called_once_with(
            params={'$where': 'name = "Trento" AND level = 60', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_where_concat(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_where_concat'])) as mock_method:
            for item in self.datagem.items.where(name='Trento').where(level=60):
                self.assertEqual(item['name'], 'Trento')
                self.assertEqual(item['level'], 60)

        mock_method.assert_called_once_with(
            params={'$where': '(name = "Trento") AND (level = 60)', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_where_greater_than_equal(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_where_greater_than_equal'])) as mock_method:
            items = self.datagem.items.select('population')
            items = items.order('population.2011')
            items = list(items.where(population__2011__gte=114063)[:50])
            self.assertTrue(
                all(x['population']['2011'] >= 114063 for x in items)
            )
            self.assertTrue(
                any(x['population']['2011'] == 114063 for x in items)
            )

        mock_method.assert_called_once_with(
            params={'$select': 'population', '$where': 'population.2011 >= 114063', '$order': 'population.2011', '$offset': 0, '$limit': 50, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_where_greater_than(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_where_greater_than'])) as mock_method:
            items = self.datagem.items.select('population')
            items = items.order('population.2011')
            items = list(items.where(population__2011__gt=114063)[:50])
            self.assertTrue(
                all(x['population']['2011'] >= 114063 for x in items)
            )
            self.assertFalse(
                any(x['population']['2011'] == 114063 for x in items)
            )

        mock_method.assert_called_once_with(
            params={'$select': 'population', '$where': 'population.2011 > 114063', '$order': 'population.2011', '$offset': 0, '$limit': 50, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_where_lower_than_equal(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_where_lower_than_equal'])) as mock_method:
            items = self.datagem.items.select('population')
            items = items.order('population.2011 DESC')
            items = list(items.where(population__2011__lte=114063)[:50])
            self.assertTrue(
                all(x['population']['2011'] <= 114063 for x in items)
            )
            self.assertTrue(
                any(x['population']['2011'] == 114063 for x in items)
            )

        mock_method.assert_called_once_with(
            params={'$select': 'population', '$where': 'population.2011 <= 114063', '$order': 'population.2011 DESC', '$offset': 0, '$limit': 50, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_where_lower_than(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_where_lower_than'])) as mock_method:
            items = self.datagem.items.select('population')
            items = items.order('population.2011 DESC')
            items = list(items.where(population__2011__lt=114063)[:50])
            self.assertTrue(
                all(x['population']['2011'] <= 114063 for x in items)
            )
            self.assertFalse(
                any(x['population']['2011'] == 114063 for x in items)
            )

        mock_method.assert_called_once_with(
            params={'$select': 'population', '$where': 'population.2011 < 114063', '$order': 'population.2011 DESC', '$offset': 0, '$limit': 50, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_where_not(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_where_not'])) as mock_method:
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

        mock_method.assert_called_once_with(
            params={'$select': 'population', '$where': '(population.2011 >= 110000) AND (population.2011 <> 114063)', '$order': 'population.2011 DESC', '$offset': 0, '$limit': 50, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_get(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_get'])) as mock_method:
            item = self.datagem.items.select('name').get(
                acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
            )
            self.assertEqual(item, dict(name='Trento'))

        mock_method.assert_called_once_with(
            params={'$select': 'name', '$where': 'acheneID = "http://dandelion.eu/resource/05a192433bede90cd0f12652b1a12c428cb253d5"', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_get_item(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_get_item'])) as mock_method:
            item = self.datagem.items.select('name').where(
                acheneID=self._achene('05a192433bede90cd0f12652b1a12c428cb253d5')
            )[0]
            self.assertEqual(item, dict(name='Trento'))

        mock_method.assert_called_once_with(
            params={'$select': 'name', '$where': 'acheneID = "http://dandelion.eu/resource/05a192433bede90cd0f12652b1a12c428cb253d5"', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_get_with_no_result(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_get_with_no_result'])) as mock_method:
            with self.assertRaises(DandelionException) as context:
                self.datagem.items.select('name').get(
                    acheneID=self._achene('42')
                )
            self.assertEqual(
                context.exception.message, 'The requested item does not exist'
            )

        mock_method.assert_called_once_with(
            params={'$select': 'name', '$where': 'acheneID = "http://dandelion.eu/resource/42"', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_order(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_order'])) as mock_method:
            items = self.datagem.items.select('population')
            items = items.order('population.2011')[:5]

            pops = [x['population']['2011'] for x in items]
            self.assertEqual(pops, sorted(pops))

        mock_method.assert_called_once_with(
            params={'$select': 'population', '$order': 'population.2011', '$offset': 0, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_order_desc(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_order_desc'])) as mock_method:
            items = self.datagem.items.select('population')
            items = items.where(population__2011__not=None)
            items = items.order('population.2011 DESC')[:5]

            pops = [x['population']['2011'] for x in items]
            self.assertEqual(pops, sorted(pops, reverse=True))

        mock_method.assert_called_once_with(
            params={'$select': 'population', '$where': 'population.2011 <> null', '$order': 'population.2011 DESC', '$offset': 0, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_limit(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_limit'])) as mock_method:
            objects = list(self.datagem.items[:5])
            self.assertEqual(len(objects), 5)

        mock_method.assert_called_once_with(
            params={'$offset': 0, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )

    def test_offset(self):
        with patch.object(sessions.Session, 'get', side_effect=(MockResponse(True, self.data['datagem_test_offset_1']), MockResponse(True, self.data['datagem_test_offset_2']), MockResponse(True, self.data['datagem_test_offset_3']))) as mock_method:
            first_half = list(self.datagem.items[:5])
            second_half = list(self.datagem.items[5:10])
            full_list = list(self.datagem.items[:10])
            self.assertEqual(first_half + second_half, full_list)

        expected_arguments = [call(
            params={'$offset': 0, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        ), call(
            params={'$offset': 5, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        ), call(
            params={'$offset': 0, '$limit': 10, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )]
        self.assertEqual(mock_method.call_args_list, expected_arguments)

    def test_pagination(self):
        with patch.object(sessions.Session, 'get', side_effect=(MockResponse(True, self.data['datagem_test_pagination_1']), MockResponse(True, self.data['datagem_test_pagination_2']))) as mock_method:
            page_size = DatagemManager.PAGINATE_BY
            items = list(self.datagem.items.select('acheneID')[:(page_size+10)])
            self.assertEqual(len(items), page_size + 10)
            self.assertEqual(
                # check pagination does not return the same item twice
                len(items), len(frozenset(x['acheneID'] for x in items))
            )

        expected_arguments = [call(
            params={'$select': 'acheneID', '$offset': 0, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        ), call(
            params={'$select': 'acheneID', '$offset': 500, '$limit': 500, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )]
        self.assertEqual(mock_method.call_args_list, expected_arguments)

    def test_step(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_step'])) as mock_method:
            items = list(self.datagem.items.select('acheneID')[:5])
            some_items = list(self.datagem.items.select('acheneID')[:5:2])
            self.assertEqual(some_items, items[::2])

        expected_arguments = [call(
            params={'$select': 'acheneID', '$offset': 0, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        ), call(
            params={'$select': 'acheneID', '$offset': 0, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )]
        self.assertEqual(mock_method.call_args_list, expected_arguments)

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
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_version'])) as mock_method:
            self.assertIsNotNone(self.datagem.version)
            self.assertEqual(len(self.datagem.version), 40)

        mock_method.assert_called_once_with(
            params={'$select': 'acheneID', '$offset': 0, '$limit': 1, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )


class TestDeprecatedCode(TestDatagemBase):
    def test_objects(self):
        with patch.object(sessions.Session, 'get', return_value=MockResponse(True, self.data['datagem_test_objects'])) as mock_method:
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

        mock_method.assert_called_once_with(
            params={'$select': 'acheneID', '$offset': 0, '$limit': 5, 'token': 'token'},
            headers={'User-Agent': 'python-dandelion-eu/0.2.2'},
            url='https://api.dandelion.eu/datagem/administrative-regions/data/v1'
        )
