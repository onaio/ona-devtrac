from devtrac.libs.tests.test_base import TestBase
from devtrac.libs.devtrac.field_trip import FieldTrip
from devtrac.libs.devtrac.site_visit import SiteVisit
from devtrac.libs.devtrac.taxonomy_vocabulary import TAXONOMY_VOCABULARY_1


class TestDevTrac(TestBase):

    def _create_field_trip(self, delete=False):
        self._drupal_login()

        ft = FieldTrip('Demo Field Trip')
        ft.add_trip_purpose(FieldTrip.OTHER, 100)
        ft.add_administrative_boundary(80)
        ft.add_start_end_date('11/03/2014', '13/03/2014')
        ft.add_proms_ta_id('UGDC/2014/03')
        ft.add_user(self.drupal.user_target_id)
        node = self.drupal.create_node(ft)

        self.assertIsInstance(node, dict)
        self.assertIn('nid', node.keys())
        self.assertIn('uri', node.keys())
        self.fieldtrip_node = node

        if delete:
            self.drupal.delete_node(node['uri'])

    def test_delete_node_not_logged_in(self):
        with self.assertRaises(Exception):
            self.drupal.delete_node("http://127.0.0.1/api/node/1.json")

    def test_field_trip_invalid_instance(self):
        self._drupal_login()

        with self.assertRaises(Exception):
            FieldTrip(None)

    def test_create_field_trip_node_tyoe_specified(self):
        self._drupal_login()

        ft = FieldTrip('Demo Field Trip', node_type='random')
        self.assertEqual(ft.node_type, 'fieldtrip')

    def test_create_field_trip(self):
        self._create_field_trip(delete=True)

    def test_create_site_visit(self):
        self._create_field_trip()
        fieldtrip = self.drupal.get_node(self.fieldtrip_node['uri'])
        target_id = u'%s (%s)' % (fieldtrip['title'], fieldtrip['nid'])
        st = SiteVisit('Visit at Place A', node_type='ftritem')
        st.set_site_visit(
            '13/03/2014', TAXONOMY_VOCABULARY_1.NGO,
            'Narrative data', 'summary data', target_id,
            location='34.114095689096 2.9995385028608')
        st._node_dict.update({'nid': fieldtrip})
        node = self.drupal.create_node(st)
        self.assertIsInstance(node, dict)
        self.assertIn('nid', node.keys())
        self.assertIn('uri', node.keys())
