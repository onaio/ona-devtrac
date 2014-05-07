import json
import requests

try:
    # python 2.7.x or below
    from urllib2 import urlparse
except ImportError:
    # python 3
    from urllib import parse as urlparse


DRUPAL_CONNECT_PATH = 'api/system/connect.json'
DRUPAL_LOGIN_PATH = 'api/user/login.json'
DRUPAL_LOGOUT_PATH = 'api/user/logout.json'
DRUPAL_NODE_PATH = 'api/node.json'


class DrupalNode(object):
    """Class to represent a Drupal Node"""

    _node_dict = None

    def __init__(self, title, node_type, value=None):
        if not isinstance(title, str):
            raise Exception(u"Expected a string for title")

        if not isinstance(node_type, str):
            raise Exception(u"Expected a string for type")

        self.title = title
        self.node_type = node_type
        if isinstance(value, str):
            self.body_value = value
        self._node_dict = {}

    def get_dict(self):
        title = getattr(self, 'title', None)
        node_type = getattr(self, 'node_type', None)
        body_value = getattr(self, 'body_value', None)

        self._node_dict.update({
            "title": title,
            "type": node_type
        })

        if body_value:
            self._node_dict['body'] = {'und': [{'value': body_value}]}
        return self._node_dict

    @property
    def json(self):
        """JSON representation of a DrupalNode"""
        return json.dumps(self.get_dict())

    def set_taxonomy_vocabulary(self, number, value, multiple=False):
        if value is None:
            return

        und_value = {'value': value}

        if multiple and isinstance(value, list):
            i = 0
            for val in value:
                if i == 0:
                    und_value['value'] = val
                else:
                    und_value['value%d' % i] = val

                i += 1

        self._node_dict.update(
            {
                'taxonomy_vocabulary_%s' % number: {
                    'und': und_value
                }
            }
        )


class Drupal(object):
    headers = {}
    host = None
    request = None

    connect_url = None
    login_url = None
    logout_url = None
    node_url = None

    token = None
    session_id = None
    session_name = None
    uid = None
    user_data = None

    def __init__(self, host="http://127.0.0.1"):
        self.host = host
        self.connect_url = urlparse.urljoin(self.host, DRUPAL_CONNECT_PATH)
        self.login_url = urlparse.urljoin(self.host, DRUPAL_LOGIN_PATH)
        self.logout_url = urlparse.urljoin(self.host, DRUPAL_LOGOUT_PATH)
        self.node_url = urlparse.urljoin(self.host, DRUPAL_NODE_PATH)
        self.user_data = {}

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
            user = data.get('user')
            if isinstance(user, dict):
                self.uid = user.get('uid')
                self.user_data = user
            self.token = data.get('token')
            self.session_id = data.get('sessid')
            self.session_name = data.get('session_name')
            self.headers['X-CSRF-Token'] = self.token
            self.headers['Content-Type'] = 'application/json'
        else:
            return False

        return True

    def create_node(self, node):
        if not isinstance(node, DrupalNode):
            raise Exception(u"node %(node)s must be of instance `Drupalnode`")

        if not self.request and self.login():
            raise Exception(u"Please Login first!")

        self.response = self.request.post(self.node_url, node.json,
                                          headers=self.headers)

        return self.response.json()

    def create_article(self, title, body):
        """Create an article node"""
        node = DrupalNode(title, 'article', body)

        return self.create_node(node)

    def modify_article(self, uri, title, body):
        """Modify an article node"""

        if not self.request and self.login():
            raise Exception(u"Please Login first!")
        node = DrupalNode(title, 'article', body)
        self.response = self.request.put(
            '%s.json' % uri, node.json, headers=self.headers)
        return self.response.json()

    def get_node(self, uri):
        """Get an article node as json"""

        if not self.request and not self.login():
            raise Exception(u"Please Login first!")

        if isinstance(uri, str) and not uri.endswith('.json'):
            uri = u'%s.json' % uri

        self.response = self.request.get(uri, headers=self.headers)

        return self.response.json()

    def get_node_list(self, parameters=None):
        """Returns a list of nodes as json"""

        if not self.request and not self.login():
            raise Exception(u"Please Login first!")

        uri = self.node_url
        if isinstance(uri, str) and not uri.endswith('.json'):
            uri = u'%s.json' % uri

        params = {}
        if isinstance(parameters, dict) and parameters:
            for key, value in parameters.items():
                params['parameters[%s]' % key] = value

        self.response = self.request.get(
            uri, params=params, headers=self.headers)

        return self.response.json()

    def delete_node(self, uri):
        """Delete a drupal node"""

        if not self.request and not self.login():
            raise Exception(u"Please Login first!")

        if isinstance(uri, str) and not uri.endswith('.json'):
            uri = u'%s.json' % uri

        self.response = self.request.delete(uri, headers=self.headers)

        return self.response.json()

    @property
    def user_target_id(self):
        return u"%s (%s)" % (self.user_data.get('realname'), self.uid)
