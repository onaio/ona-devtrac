import json

from django.test import TestCase

from devtrac.libs.drupal import Drupal, DrupalNode


class TestDrupal(TestCase):

    def setUp(self):
        self.drupal = Drupal()

    def _drupal_login(self):
        self.assertIsNone(self.drupal.token)
        self.assertIsNone(self.drupal.session_id)

        self.drupal.login(username='api_user', password='api_pass')

        self.assertEqual(self.drupal.response.status_code, 200)
        self.assertIsNotNone(self.drupal.token)
        self.assertIsNotNone(self.drupal.session_id)

    def test_connect_anonymous_user(self):
        response = self.drupal.connect()
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"uid":0,"hostname":"127.0.0.1",'
                      '"roles":{"1":"anonymous user"}', response.text)

    def test_login_failed(self):
        self.drupal.login(username='demo', password='wrong_pass')
        self.assertTrue(self.drupal.response.status_code, 401)

    def test_login_success(self):
        self._drupal_login()

    def test_connect_user(self):
        self._drupal_login()
        response = self.drupal.connect()
        self.assertEqual(response.status_code, 200)
        self.assertIn('"name":"api_user"', response.text)


class TestDrupalNode(TestCase):
    def test_drupalnode(self):
        title = 'Title'
        node_type = 'article'
        notes = 'A lot of text for the budy'
        node = DrupalNode(title, node_type, notes)
        json_str = '{"title": "Title", "bnd": [{"value":'\
            ' "A lot of text for the budy"}], "type": "article"}'
        self.assertEqual(json.loads(node.json), json.loads(json_str))

    def test_drupalnode_invalid_title(self):
        node = DrupalNode(None, 'article')
        with self.assertRaises(Exception):
            node.json

    def test_drupalnode_invalid_node_type(self):
        node = DrupalNode('title', None)
        with self.assertRaises(Exception):
            node.json
