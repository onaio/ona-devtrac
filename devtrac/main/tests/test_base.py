from django.test import TestCase

from devtrac.main.models import Submission


class TestBase(TestCase):
    def _add_submission(self):
        data = {"_id": 2, "name": "submission"}
        submission = Submission(data=data, processed=True)
        submission.save()
        self.assertEqual(submission, Submission.objects.get(pk=submission.pk))
