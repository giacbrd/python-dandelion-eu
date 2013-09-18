""" dandelion datagem
"""
import urlparse
import requests

from dandelion import DandelionException


class Datagem(object):
    """ a datagem, aka a source of data on dandelion
    """
    DANDELION_HOST = 'dandelion.eu'

    def __init__(self, uid, host=None):
        self.uid = uid
        self.uri = self._get_uri(host=host)

    def _get_uri(self, host=None):
        base_uri = 'https://' + (host or self.DANDELION_HOST)
        return urlparse.urljoin(
            base_uri, '/'.join(['api', 'v1', 'datagem', self.uid, 'data.json'])
        )

    @property
    def objects(self):
        return DatagemManager(self)


class DatagemManager(object):
    """ an object responsible for retrieving data form a datagem
    """
    PAGINATE_BY = 500

    def __init__(self, datagem):
        self.datagem = datagem
        self.params = {}
        self._step = 1
        self._stop = None

    def filter(self, **kwargs):
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
        return self.filter(**kwargs).__iter__().next()

    def values(self, *args):
        self.params['$select'] = ','.join(args)
        return self

    def __iter__(self):
        offset = self.params.get('$offset', 0)
        returned = 0
        while True:
            params = dict(self.params)
            params['$limit'] = min(self.PAGINATE_BY, self.params.get('$limit', self.PAGINATE_BY))
            params['$offset'] = offset
            response = requests.get(
                self.datagem.uri,
                params=params,
                verify=False,
            )

            if not response.ok:
                raise DandelionException(response.json()['message'])

            for obj in response.json():
                if returned % self._step == 0:
                    yield obj
                returned += 1
                if self._stop and returned >= self._stop:
                    raise StopIteration

            if len(response.json()) < self.PAGINATE_BY:
                raise StopIteration
            offset += self.PAGINATE_BY

    def __getitem__(self, item):
        if isinstance(item, int):
            self.params['$offset'] = item
            return self.get()

        if not isinstance(item, slice):
            raise TypeError("Invalid type {}".format(type(item)))

        self.params['$offset'] = item.start if item.start else 0
        self._stop = item.stop - self.params['$offset']
        self._step = item.step if item.step else 1
        self.params['$limit'] = self._stop

        if self._stop <= 0:
            raise TypeError('Unsupported negative indexes')
        return self

    @staticmethod
    def _parse_single_filter(key, value):
        """ prepare a value for being used in the api
        """
        if isinstance(value, basestring):
            value = '"%s"' % value

        operator = '='
        tokens = key.split('__')
        if len(tokens) > 2:
            raise DandelionException("Invalid key operator")
        if len(tokens) == 2:
            key = tokens[0]
            if tokens[1] == 'lte':
                operator = '<='
            elif tokens[1] == 'lt':
                operator = '<'
            elif tokens[1] == 'gt':
                operator = '>'
            elif tokens[1] == 'gte':
                operator = '>='
            elif tokens[1] == 'not':
                operator = '<>'

        return '{} {} {}'.format(key, operator, value)
