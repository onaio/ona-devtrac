from django.test import TestCase, RequestFactory

from devtrac.main.models import Submission
from devtrac.main.views import SubmissionPostView


class SubmissionPostTest(TestCase):
    def test_post_json_submission(self):
        count = Submission.objects.count()
        data = {"_id": 2, "name": "submission"}
        factory = RequestFactory()
        request = factory.post('/', data=data)
        view = SubmissionPostView.as_view()
        response = view(request)

        self.assertContains(response, '"message": "success"')
        self.assertEqual(count + 1, Submission.objects.count())
