import os

try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle

from dandelion.cache import NoCache


class FileCache(NoCache):
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        assert os.path.isdir(self.cache_dir), \
            "{} exists but is not a directory".format(self.cache_dir)

    def _get_filename_for(self, key):
        return os.path.join(self.cache_dir, key)

    def contains_key(self, key):
        return os.path.isfile(self._get_filename_for(key))

    def get(self, key):
        with open(self._get_filename_for(key), 'rb') as fin:
            return pickle.load(fin)

    def set(self, key, value):
        with open(self._get_filename_for(key), 'wb') as fout:
            return pickle.dump(value, fout, pickle.HIGHEST_PROTOCOL)
