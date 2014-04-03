import json

from django.http import HttpResponse
from django.views.generic import View

from devtrac.main.models import Submission
from devtrac.libs.views.mixins import CSRFExemptMixin


class SubmissionPostView(CSRFExemptMixin, View):
    def post(self, *args, **kwargs):
        response = {'status': 200, 'message': 'success'}
        data = json.loads(self.request.body.decode())
        Submission.objects.create(data=data)

        return HttpResponse(json.dumps(response),
                            content_type='application/json')
