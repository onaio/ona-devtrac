import csv
import json

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View, TemplateView

from devtrac.main.models import Submission
from devtrac.libs.views.mixins import CSRFExemptMixin
from devtrac.libs.utils import process_json_submission
from devtrac.libs.drupal import Drupal
from devtrac.libs.devtrac.constants import TYPE_FIELDTRIP, TYPE_PLACE


def get_drupal_object():
    drupal = Drupal(settings.DRUPAL_HOST)
    drupal.login(settings.DRUPAL_USERNAME, settings.DRUPAL_PASSWORD)
    return drupal


def post_submission_to_devtrac(submission):
    drupal = get_drupal_object()
    response = process_json_submission(drupal, submission.data,
                                       settings.TEST_FIELD_TRIP)

    if isinstance(response, dict) and 'nid' in response:
        submission.nid = response['nid']
        submission.uri = response['uri']
        submission.processed = True
        submission.save()

    return submission


def get_fieldtrips():
    drupal = get_drupal_object()
    data = drupal.get_node_list(
        parameters={'type': TYPE_FIELDTRIP, 'uid': drupal.uid})
    return data


def get_places():
    drupal = get_drupal_object()
    data = drupal.get_node_list(
        parameters={'type': TYPE_PLACE})
    return data


def get_nodes_csv_response(nodes, name, headers, fields):
    response = HttpResponse(content_type='text/csv')
    response['Content-Desposition'] = 'attachment; filename=%s.csv' % name

    assert type(nodes) is list
    assert type(headers) is list
    assert type(fields) is list

    writer = csv.writer(response)
    writer.writerow(headers)

    for node in nodes:
        row = [u'%(title)s (%(nid)s)' % node] + \
            [node[field] for field in fields]
        writer.writerow(row)

    return response


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


class FieldTripsView(View):
    def get(self, *args, **kwargs):
        headers = ['fieldtrip_key', 'nid', 'title']
        fields = ['nid', 'title']

        return get_nodes_csv_response(
            get_fieldtrips(), 'fieldtrips', headers, fields)


class PlacesView(View):
    def get(self, *args, **kwargs):
        headers = ['place_key', 'nid', 'title']
        fields = ['nid', 'title']

        return get_nodes_csv_response(
            get_fieldtrips(), 'places', headers, fields)
