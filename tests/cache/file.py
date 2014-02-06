import os
from tempfile import mkdtemp
from shutil import rmtree
from unittest import TestCase

from mock import MagicMock

from dandelion.cache import FileCache
from .base import CacheBaseMixin, FakeDandelionRequest


class TestFileCache(CacheBaseMixin, TestCase):

    def setUp(self):
        self.cache_dir = mkdtemp()
        self.req_obj = FakeDandelionRequest(cache=FileCache(self.cache_dir))

    def tearDown(self):
        rmtree(self.cache_dir)


class TestFileCacheNonExistingDir(CacheBaseMixin, TestCase):

    def setUp(self):
        self.cache_root = mkdtemp()
        self.cache_dir = os.path.join(self.cache_root, 'subdirectory')
        self.req_obj = FakeDandelionRequest(cache=FileCache(self.cache_dir))

    def tearDown(self):
        rmtree(self.cache_root)
