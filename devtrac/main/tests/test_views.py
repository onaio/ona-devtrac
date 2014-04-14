import os
import json

from django.conf import settings
from django.test import RequestFactory

from devtrac.main.models import Submission
from devtrac.main.views import SubmissionPostView, post_submission_to_devtrac
from devtrac.main.tests.test_base import TestBase


class SubmissionPostTest(TestBase):
    def test_post_json_submission(self):
        count = Submission.objects.count()
        data = '{"_id": 2, "name": "submission"}'
        factory = RequestFactory()
        request = factory.post('/', data, 'application/json')
        view = SubmissionPostView.as_view()
        response = view(request)

        self.assertContains(response, '"message": "success"')
        self.assertEqual(count + 1, Submission.objects.count())

    def test_post_invalid_submission_to_devtrac(self):
        submission = self._add_submission()
        self.assertIsNone(submission.nid)
        self.assertIsNone(submission.uri)
        self.assertFalse(submission.processed)

        submission = post_submission_to_devtrac(submission)
        self.assertIsNone(submission.nid)
        self.assertIsNone(submission.uri)
        self.assertFalse(submission.processed)

    def test_post_submission_to_devtrac(self):
        data = json.load(open(os.path.join(settings.BASE_DIR, 'devtrac',
                                           'libs', 'tests', 'fixtures',
                                           'site_visit_report.json')))
        submission = self._add_submission(data=data)
        self.assertIsNone(submission.nid)
        self.assertIsNone(submission.uri)
        self.assertFalse(submission.processed)

        submission = post_submission_to_devtrac(submission)
        self.assertIsNotNone(submission.nid)
        self.assertIsNotNone(submission.uri)
        self.assertTrue(submission.processed)
