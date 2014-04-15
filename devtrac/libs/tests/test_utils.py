import json
import os
import warnings

from devtrac.libs.tests.test_base import TestBase
from devtrac.libs import utils
from django.conf import settings


class TestUtils(TestBase):
    field_trip = settings.TEST_FIELD_TRIP

    def test_process_site_visit_submission(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'site_visit_report.json')))
        response = utils.process_json_submission(self.drupal, data,
                                                 self.field_trip)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])

    def test_process_roadside_submission_null_taxonomy_8(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'roadside_report_50368.json')))
        response = utils.process_json_submission(self.drupal, data,
                                                 self.field_trip)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])

    def test_process_roadside_submission(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'roadside_report.json')))
        response = utils.process_json_submission(self.drupal, data,
                                                 self.field_trip)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])

    def test_process_human_interest_submission(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'human_interest.json')))
        response = utils.process_json_submission(self.drupal, data,
                                                 self.field_trip)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])
