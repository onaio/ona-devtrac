import json
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


class DrupalNode(object):
    """Class to represent a Drupal Node"""
    def __init__(self, title, node_type, value=None):
        if not isinstance(title, str):
            raise Exception(u"Expected a string for title")

        if not isinstance(node_type, str):
            raise Exception(u"Expected a string for type")

        self.title = title
        self.node_type = node_type
        if isinstance(value, str):
            self.body_value = value

    @property
    def json(self):
        """JSON representation of a DrupalNode"""
        title = getattr(self, 'title')
        node_type = getattr(self, 'node_type')
        body_value = getattr(self, 'body_value')

        obj = {
            "title": title,
            "type": node_type
        }

        if body_value:
            obj['bnd'] = [{'value': body_value}]

        return json.dumps(obj)
