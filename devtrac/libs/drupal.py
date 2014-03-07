import requests

from urllib.parse import urljoin


DRUPAL_CONNECT_PATH = 'api/system/connect.json'


class Drupal(object):
    host = None
    connect_url = None

    def __init__(self, host="http://127.0.0.1"):
        self.host = host
        self.connect_url = urljoin(self.host, DRUPAL_CONNECT_PATH)

    def connect(self):
        self.response = requests.post(self.connect_url)
        return self.response
