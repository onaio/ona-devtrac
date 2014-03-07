import requests

from urllib.parse import urljoin


DRUPAL_CONNECT_PATH = 'api/system/connect.json'
DRUPAL_LOGIN_PATH = 'api/user/login.json'
DRUPAL_LOGOUT_PATH = 'api/user/logout.json'


class Drupal(object):
    headers = {}
    host = None
    request = None

    connect_url = None
    login_url = None
    logout_url = None

    token = None
    session_id = None
    session_name = None
    uid = None

    def __init__(self, host="http://127.0.0.1"):
        self.host = host
        self.connect_url = urljoin(self.host, DRUPAL_CONNECT_PATH)
        self.login_url = urljoin(self.host, DRUPAL_LOGIN_PATH)
        self.logout_url = urljoin(self.host, DRUPAL_LOGOUT_PATH)

    def connect(self):
        if self.request is not None and self.headers:
            self.response = self.request.post(self.connect_url,
                                              headers=self.headers)
        else:
            self.response = requests.post(self.connect_url)
        return self.response

    def login(self, username='api_user', password='api_pass'):
        data = {'username': username, 'password': password}
        self.request = requests.Session()
        self.response = self.request.post(self.login_url, data)
        if self.response.status_code == 200:
            data = self.response.json()
            self.uid = data.get('uid')
            self.token = data.get('token')
            self.session_id = data.get('sessid')
            self.session_name = data.get('session_name')
            self.headers['X-CSRF-Token'] = self.token
        else:
            return False
        return True
