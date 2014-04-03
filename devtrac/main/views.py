import json

from django.http import HttpResponse
from django.views.generic import View


class SubmissionPostView(View):
    def post(self, *args, **kwargs):
        data = {'status': 200, 'message': 'success'}
        return HttpResponse(json.dumps(data), content_type='application/json')
