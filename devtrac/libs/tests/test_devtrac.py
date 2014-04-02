from devtrac.libs.tests.test_base import TestBase
from devtrac.libs.devtrac.site_visit import SiteVisit
from devtrac.libs.devtrac.taxonomy_vocabulary import TAXONOMY_VOCABULARY_1


class TestDevTrac(TestBase):

    def test_delete_node_not_logged_in(self):
        with self.assertRaises(Exception):
            self.drupal.delete_node("http://127.0.0.1/api/node/1.json")

    def test_create_site_visit(self):
        self._drupal_login()
        self.fieldtrip_node = {'uri': 'http://jenkinsge.mountbatten.net/'
                               'devtracmanual/api/node/14997.json',
                               'nid': '14997'}
        fieldtrip = self.drupal.get_node(self.fieldtrip_node['uri'])
        target_id = u'%s (%s)' % (fieldtrip['title'], fieldtrip['nid'])
        place = u'%s (%s)' % ('UMSC Office Kotido', '5547')
        st = SiteVisit('Visit at Place A', node_type='ftritem')
        st.set_site_visit(
            '13/03/2014', TAXONOMY_VOCABULARY_1.NGO,
            'Narrative data', 'summary data', target_id,
            location='34.114095689096 2.9995385028608',
            place=place)
        st._node_dict.update({'nid': fieldtrip})
        node = self.drupal.create_node(st)
        self.assertIsInstance(node, dict)
        self.assertIn('nid', node.keys())
        self.assertIn('uri', node.keys())
