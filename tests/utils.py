import json


class MockResponse:
    def __init__(self, ok, resp_data):
        self.ok = ok
        self.resp_data = resp_data

    def json(self, object_hook=None):
        return json.loads(self.resp_data, object_hook=object_hook)
