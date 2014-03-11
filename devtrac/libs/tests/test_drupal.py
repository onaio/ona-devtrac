import json

from django.conf import settings
from django.test import TestCase

from devtrac.libs.drupal import Drupal, DrupalNode


class TestDrupal(TestCase):

    def setUp(self):
        self.drupal = Drupal(settings.DRUPAL_HOST)

    def _drupal_login(self, username=settings.DRUPAL_USERNAME,
                      password=settings.DRUPAL_PASSWORD):
        self.assertIsNone(self.drupal.token)
        self.assertIsNone(self.drupal.session_id)

        self.drupal.login(username=username, password=password)

        self.assertEqual(self.drupal.response.status_code, 200)
        self.assertIsNotNone(self.drupal.token)
        self.assertIsNotNone(self.drupal.session_id)

    def _add_article(self, title='Title', body="Body"):
        self._drupal_login()
        article = self.drupal.create_article(title, body)
        # skip test if user has no permission
        if isinstance(article, list):
            if article[0].startswith('Access denied for user'):
                self.skipTest(article[0])
        self.assertIsInstance(article, dict)
        self.assertIn('nid', article.keys())
        self.assertIn('uri', article.keys())
        self.article = article

        return self.article

    def test_connect_anonymous_user(self):
        response = self.drupal.connect()
        self.assertEqual(response.status_code, 200)
        self.assertIn('"roles":{"1":"anonymous user"}', response.text)

    def test_login_failed(self):
        self.drupal.login(username='demo', password='wrong_pass')
        self.assertTrue(self.drupal.response.status_code, 401)

    def test_login_success(self):
        self._drupal_login()

    def test_connect_user(self):
        self._drupal_login()
        response = self.drupal.connect()
        self.assertEqual(response.status_code, 200)
        self.assertIn('"name":"%s"' % settings.DRUPAL_USERNAME, response.text)

    def test_create_article(self):
        self._add_article()

    def test_get_article(self):
        self._add_article()
        uri = self.article['uri']
        node = self.drupal.get_article(uri)
        self.assertEqual(node['path'], uri.replace('api/', ''))
        self.assertEqual(node['title'], 'Title')

    def test_modify_article(self):
        self._add_article()
        uri = self.article['uri']
        title = 'Test Title Edited'
        body = 'Test Body for article Edited'
        article = self.drupal.modify_article(uri, title, body)
        self.assertEqual(article['uri'], uri)
        article = self.drupal.get_article(uri)
        self.assertEqual(title, article['title'])

    def test_delete_article(self):
        self._add_article()
        uri = self.article['uri']
        success = self.drupal.delete_article(uri)
        self.assertEqual(success, [True])

    def tearDown(self):
        if hasattr(self, 'drupal') and hasattr(self, 'article'):
            self.drupal.delete_article(self.article['uri'])


class TestDrupalNode(TestCase):
    def test_drupalnode(self):
        title = 'Title'
        node_type = 'article'
        notes = 'A lot of text for the budy'
        node = DrupalNode(title, node_type, notes)
        json_str = '{"title": "Title", "body": {"und": [{"value":'\
            ' "A lot of text for the budy"}]}, "type": "article"}'
        self.assertEqual(json.loads(node.json), json.loads(json_str))

    def test_drupalnode_invalid_title(self):
        with self.assertRaises(Exception):
            DrupalNode(None, 'article')

    def test_drupalnode_invalid_node_type(self):
        with self.assertRaises(Exception):
            DrupalNode('title', None)
