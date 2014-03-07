from django.test import TestCase

from devtrac.libs.drupal import Drupal


class TestDrupal(TestCase):

    def setUp(self):
        self.drupal = Drupal()

    def test_connect_anonymous_user(self):
        response = self.drupal.connect()
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"uid":0,"hostname":"127.0.0.1",'
                      '"roles":{"1":"anonymous user"}', response.text)
