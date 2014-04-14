import json

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View, TemplateView

from devtrac.main.models import Submission
from devtrac.libs.views.mixins import CSRFExemptMixin
from devtrac.libs.utils import process_json_submission
from devtrac.libs.drupal import Drupal


def post_submission_to_devtrac(submission):
    drupal = Drupal(settings.DRUPAL_HOST)
    drupal.login(settings.DRUPAL_USERNAME, settings.DRUPAL_PASSWORD)
    response = process_json_submission(drupal, submission.data,
                                       settings.TEST_FIELD_TRIP)

    if isinstance(response, dict) and 'nid' in response:
        submission.nid = response['nid']
        submission.uri = response['uri']
        submission.processed = True
        submission.save()

    return submission


class SubmissionPostView(CSRFExemptMixin, View):
    def post(self, *args, **kwargs):
        response = {'status': 200, 'message': 'success'}
        data = json.loads(self.request.body.decode())
        submission = Submission.objects.create(data=data)
        post_submission_to_devtrac(submission)

        return HttpResponse(json.dumps(response),
                            content_type='application/json')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, *args, **kwargs):
        submissions = Submission.objects.filter()
        total_submissions = submissions.count()
        processed = submissions.filter(processed=True)
        num_processed = processed.count()
        kwargs.update({
            'submissions': submissions,
            'total_submissions': total_submissions,
            'num_processed': num_processed,
            'ona_api_uri': settings.ONA_API_URI_DEVTRAC
        })
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
