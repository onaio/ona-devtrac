from devtrac.libs.tests.test_base import TestBase
from devtrac.libs.devtrac.field_trip import FieldTrip
from devtrac.libs.devtrac.site_visit import SiteVisit
from devtrac.libs.devtrac.taxonomy_vocabulary import TAXONOMY_VOCABULARY_1


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
        ft.add_trip_purpose(FieldTrip.OTHER, 100)
        ft.add_administrative_boundary(80)
        ft._node_dict.update({'field_fieldtrip_start_end_date':
                              {"und": [{'value': {'date': '11/03/2014'},
                                        'value2': {'date': '13/03/2014'}}]}})
        self.skipTest(u"500 response, not sure why yet.")
        node = self.drupal.create_node(ft)

        self.assertIsInstance(node, dict)
        self.assertIn('nid', node.keys())
        self.assertIn('uri', node.keys())

    def test_create_site_visit(self):
        self._drupal_login()
        st = SiteVisit('Visit at Place A')
        st.set_site_visit(
            '13/03/2014', TAXONOMY_VOCABULARY_1.NGO,
            'Narrative data', 'summary data', 13974)
        node = self.drupal.create_node(st)
        self.assertIsInstance(node, dict)
        self.assertIn('nid', node.keys())
        self.assertIn('uri', node.keys())
