""" dandelion datagem
"""
from __future__ import unicode_literals

import warnings
import six

from dandelion.base import DandelionException, BaseDandelionRequest


class Datagem(BaseDandelionRequest):
    """ a datagem, aka a source of data on dandelion
    """

    def __init__(self, uid, **kwargs):
        self.uid = uid
        super(Datagem, self).__init__(**kwargs)

    def _get_uri_tokens(self):
        return 'datagem', self.uid, 'data/v1'

    @property
    def items(self):
        return DatagemManager(self)

    @property
    def objects(self):
        warnings.warn(
            '"objects" is deprecated, use "items" instead', DeprecationWarning
        )
        return DatagemManager(self)

    def _do_raw_request(self, url, params, **kwargs):
        return self.requests.get(
            url=url, params=params, **kwargs
        )


class DatagemManager(object):
    """ an object responsible for retrieving data form a datagem
    """
    PAGINATE_BY = 500

    def __init__(self, datagem):
        self.datagem = datagem
        self.params = {}
        self._step = 1

    def where(self, **kwargs):
        if not kwargs:
            return self

        new_filter = ' AND '.join(
            self._parse_single_filter(key, value)
            for key, value in kwargs.items()
        )
        if '$where' not in self.params:
            self.params['$where'] = new_filter
        else:
            self.params['$where'] = '({}) AND ({})'.format(
                self.params['$where'], new_filter
            )

        return self

    def get(self, **kwargs):
        try:
            return next(self.where(**kwargs).__iter__())
        except StopIteration:
            raise DandelionException('The requested item does not exist')

    def select(self, *args):
        self.params['$select'] = ','.join(args)
        if any(param.startswith('count(') for param in args):
            self.params['$group'] = ','.join(
                param for param in args if not param.startswith('count(')
            )
        return self

    def order(self, *args):
        self.params['$order'] = ','.join(args)
        return self

    def __iter__(self):
        offset = self.params.get('$offset', 0)
        returned = 0
        actual_limit = self.params.get('$limit', None)
        while True:
            params = dict(self.params)
            params['$limit'] = min(
                self.PAGINATE_BY, actual_limit or self.PAGINATE_BY
            )
            params['$offset'] = offset
            response = self.datagem.do_request(params)

            for obj in response['items']:
                if returned % self._step == 0:
                    yield obj
                returned += 1
                if actual_limit and returned >= actual_limit:
                    raise StopIteration

            if len(response['items']) < self.PAGINATE_BY:
                raise StopIteration
            offset += self.PAGINATE_BY

    def __getitem__(self, item):
        if isinstance(item, int):
            if item < 0:
                raise TypeError('Negative indexes are not supported')
            self.params['$offset'] = item
            return self.get()

        if not issubclass(type(item), slice):
            raise TypeError("Invalid slice type: {}".format(type(item)))

        self.params['$offset'] = item.start if item.start else 0
        self.params['$limit'] = None if item.stop is None \
            else item.stop - self.params['$offset']
        self._step = item.step if item.step is not None else 1

        if self.params['$offset'] < 0:
            raise TypeError('Negative indexes are not supported')
        if self.params['$limit'] is not None and self.params['$limit'] <= 0:
            raise TypeError('Negative indexes are not supported')
        if self._step <= 0:
            raise TypeError('Non-positive step is not supported')
        return self

    @staticmethod
    def _parse_single_filter(key, value):
        """ prepare a value for being used in the api
        """
        if isinstance(value, six.string_types):
            value = '"%s"' % value
        if value is None:
            value = 'null'

        operator = '='
        tokens = key.split('__')
        key_last_index = None
        if len(tokens) > 1:
            key_last_index = -1
            if tokens[-1] == 'lte':
                operator = '<='
            elif tokens[-1] == 'lt':
                operator = '<'
            elif tokens[-1] == 'gt':
                operator = '>'
            elif tokens[-1] == 'gte':
                operator = '>='
            elif tokens[-1] == 'not':
                operator = '<>'
            else:
                key_last_index = None

        key = '.'.join(tokens[:key_last_index])
        return '{} {} {}'.format(key, operator, value)
