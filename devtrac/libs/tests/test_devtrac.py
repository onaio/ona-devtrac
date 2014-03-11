from devtrac.libs.tests.test_base import TestBase
from devtrac.libs.devtrac import FieldTrip


class TestDevTrac(TestBase):
    def test_field_trip_invalid_instance(self):
        self._drupal_login()

        with self.assertRaises(Exception):
            FieldTrip(None)

    def test_create_field_trip_node_tyoe_specified(self):
        self._drupal_login()

        ft = FieldTrip('Demo Field Trip', node_type='random')
        self.assertEqual(ft.node_type, 'fieldtrip')

    def test_create_field_trip(self):
        self._drupal_login()

        ft = FieldTrip('Demo Field Trip')
        node = self.drupal.create_node(ft)

        self.assertIsInstance(node, dict)
        self.assertIn('nid', node.keys())
        self.assertIn('uri', node.keys())
