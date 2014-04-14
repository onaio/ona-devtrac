from django.test import TestCase

from devtrac.main.models import Submission


class TestBase(TestCase):
    def _add_submission(self,
                        data={"_id": 2, "name": "submission"},
                        processed=False):
        submission = Submission(data=data, processed=processed)
        submission.save()
        self.assertEqual(submission, Submission.objects.get(pk=submission.pk))
        return submission
