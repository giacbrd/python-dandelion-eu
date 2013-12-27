import hashlib


class NoCache(object):
    def contains_key(self, key):
        return False

    def get(self, key):
        raise NotImplemented

    def set(self, key, value):
        pass

    @staticmethod
    def get_key_for(**kwargs):
        input_s = ''
        for key in sorted(kwargs):
            input_s += '{}={},'.format(key, kwargs[key])
        return hashlib.sha1(input_s).hexdigest()
