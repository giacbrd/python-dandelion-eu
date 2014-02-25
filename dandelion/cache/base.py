import hashlib


class NoCache(object):
    def contains_key(self, key):
        return False

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value):
        pass

    @staticmethod
    def get_key_for(**kwargs):
        import six
        input_s = ''
        for key in sorted(kwargs):
            input_s += '{}={},'.format(key, kwargs[key])
        if isinstance(input_s, six.text_type):
            input_s = input_s.encode('utf-8')
        return hashlib.sha1(input_s).hexdigest()
