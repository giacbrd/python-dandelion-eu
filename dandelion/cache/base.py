import hashlib


class NoCache(object):
    def contains_key(self, key):
        return False

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value):
        pass

    @classmethod
    def _key_for_map(cls, map):
        input_s = ''
        for key in sorted(map):
            input_s += u'{}={},'.format(key, cls._key_for_map(map[key]) if isinstance(map[key], dict) else map[key])
        return input_s

    @classmethod
    def get_key_for(cls, **kwargs):
        import six
        input_s = cls._key_for_map(kwargs)
        if isinstance(input_s, six.text_type):
            input_s = input_s.encode('utf-8')
        return hashlib.sha1(input_s).hexdigest()
