import json
import os

from devtrac.libs.tests.test_base import TestBase
from devtrac.libs import utils


class TestUtils(TestBase):
    def test_process_site_visit_submission(self):
        self._drupal_login()

        fieldtrip_id = 'Devtrac Trip (15074)'
        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'site_visit_report.json')))
        response = utils.process_json_submission(self.drupal, data,
                                                 fieldtrip_id)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
