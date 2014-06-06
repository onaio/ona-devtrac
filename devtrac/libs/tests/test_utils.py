import json
import os
import warnings

from datetime import datetime
from django.utils import six
from devtrac.libs.tests.test_base import TestBase
from devtrac.libs import utils
from django.conf import settings


class TestUtils(TestBase):
    field_trip = settings.TEST_FIELD_TRIP

    def test_process_site_visit_submission(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'site_visit_report.json')))
        date_visited = datetime.now().strftime('%Y-%m-%d')
        response = utils.process_json_submission(self.drupal, data,
                                                 date_visited)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])

    def test_process_roadside_submission(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'roadside_report.json')))
        date_visited = datetime.now().strftime('%Y-%m-%d')
        response = utils.process_json_submission(self.drupal, data,
                                                 date_visited)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])

    def test_process_human_interest_submission(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'human_interest.json')))
        date_visited = datetime.now().strftime('%Y-%m-%d')
        response = utils.process_json_submission(self.drupal, data,
                                                 date_visited)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])

    def test_get_file_from_ona(self):
        filename = "1401788570553.jpg"
        data = utils.get_file_from_ona(filename)
        self.assertTrue(isinstance(data, six.string_types))

    def test_process_submission_with_questionaires(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'questionnaires.json')))
        date_visited = datetime.now().strftime('%Y-%m-%d')
        response = utils.process_json_submission(self.drupal, data,
                                                 date_visited)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])
        q_id = utils.process_questions(self.drupal, response, data)
        self.assertIsInstance(q_id, list)
        self.assertTrue(q_id[0].isnumeric())

    def test_process_submission_with_no_questionaires(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'no_questionnaire.json')))
        date_visited = datetime.now().strftime('%Y-%m-%d')
        response = utils.process_json_submission(self.drupal, data,
                                                 date_visited)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])
        q_id = utils.process_questions(self.drupal, response, data)
        self.assertIsNone(q_id)

    def test_process_submission_with_no_image(self):
        self._drupal_login()

        data = json.load(open(os.path.join(self.fixtures_dir,
                                           'noimage.json')))
        date_visited = datetime.now().strftime('%Y-%m-%d')
        response = utils.process_json_submission(self.drupal, data,
                                                 date_visited)
        self.assertIsInstance(response, dict)
        self.assertIn('uri', response)
        self.assertIn('nid', response)
        warnings.warn(response['uri'])
