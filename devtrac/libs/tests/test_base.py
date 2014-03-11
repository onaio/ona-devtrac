from django.conf import settings
from django.test import TestCase

from devtrac.libs.drupal import Drupal


class TestBase(TestCase):

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

    def tearDown(self):
        if hasattr(self, 'drupal') and hasattr(self, 'article'):
            self.drupal.delete_article(self.article['uri'])
