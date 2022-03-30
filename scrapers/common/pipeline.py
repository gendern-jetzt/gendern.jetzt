import requests


class Pipeline:
    def __init__(self, host):
        self.host = host

    def add_texts(self, texts):
        req = requests.post(f"{self.host}/add_texts", json=texts)
        assert req.status_code == 200
        return req.json()
