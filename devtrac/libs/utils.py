import base64
import json
import requests

from datetime import datetime

from django.conf import settings

from devtrac.libs.drupal import Drupal
from devtrac.libs.devtrac.site_visit import SiteReport
from devtrac.libs.devtrac import constants

SITE_VISIT_REPORT = '0'
ROAD_SIDE_REPORT = '1'
HUMAN_INTEREST_REPORT = '2'


def _get_long_lat_string(lat_long_str):
    """Gets a string "latitude longitude"

    returns a string "longitude latitude"
    """
    if len(lat_long_str.split()) > 1:
        tmp = lat_long_str.split(' ')[:2]
        tmp.reverse()
        return u' '.join(tmp)

    return None


def get_file_from_ona(filename):
    """Download attachment files from ona.io
    return a base64 string of the file"""
    uri = "https://ona.io/attachment/original?media_file=%s"
    file_path = "devtrac/attachments/%s" % filename
    response = requests.get(uri % file_path)

    return base64.b64encode(response.content).decode()


def upload_files(files, drupal):
    uploaded = []

    if isinstance(files, list):
        for f in files:
            filename = f['photos/report_photo']
            data = {"file": get_file_from_ona(filename),
                    "filename": filename}
            fid = drupal._upload_file_json(data)

            if isinstance(fid, dict) and 'fid' in fid:
                uploaded.append({'fid': fid['fid']})

    return uploaded


def process_site_report_submission(data, date_visited=None, drupal=None):
    """Return a SiteVisit drupal node for processing with devtrac site"""

    fieldtrip = data.get('fieldtrip')
    field_place_lat_long = data.get('lat_long')
    title = data.get('title')
    taxonomy_vocabulary_1 = data.get('location_type')
    taxonomy_vocabulary_6 = data.get('district')
    taxonomy_vocabulary_7 = data.get('site_report_type')
    taxonomy_vocabulary_8 = data.get('sector')
    date_visited = date_visited if date_visited else \
        data.get('date_visited')
    place = data.get('place')
    summary = data.get('summary')
    narrative = data.get('narrative')
    photos = data.get('photos')

    site_report = SiteReport(title)

    if isinstance(field_place_lat_long, str) and len(field_place_lat_long):
        location = _get_long_lat_string(field_place_lat_long)
        if location is not None:
            site_report.set_location(location)

    if isinstance(date_visited, str):
        date_visited = datetime.strptime(date_visited, '%Y-%m-%d')
        site_report.set_date_visited(date_visited.strftime('%d/%m/%Y'))

    if isinstance(taxonomy_vocabulary_8, str):
        taxonomy_vocabulary_8 = taxonomy_vocabulary_8.split(' ')

    if place:
        site_report.set_place(place)

    site_report.set_taxonomy_vocabulary(1, taxonomy_vocabulary_1)
    site_report.set_taxonomy_vocabulary(6, taxonomy_vocabulary_6)
    site_report.set_taxonomy_vocabulary(7, taxonomy_vocabulary_7)
    site_report.set_taxonomy_vocabulary(8, taxonomy_vocabulary_8,
                                        multiple=True)
    site_report.set_public_summary(summary)
    site_report.set_narrative(narrative)
    site_report.set_field_trip(fieldtrip)
    site_report.set_images(upload_files(photos, drupal))

    return site_report


def process_json_submission(drupal, data, date_visited=None):
    """Receives a json string from an odk submission,
    then creates appropriate Site report
    """
    if isinstance(data, str):
        data = json.loads(data)

    if not isinstance(data, dict):
        raise Exception(u"Expecting dictionary for `data` parameter")

    node = process_site_report_submission(data, date_visited, drupal)

    if node is not None:
        return drupal.create_node(node)

    return None


def get_question_value(q_num, value):
    """Get value to send to devtrac from constants.answer_options"""
    question = constants.questions.get(q_num)

    if isinstance(question, dict):
        q_type = question.get('type')

        if q_type in ['select', 'radios']:
            value = question.get('options').get(value, value)
        elif q_type == 'checkboxes':
            _value = {}
            for val in value.split(' '):
                key = question.get('options').get(val, val)
                _value[key] = key
            value = _value
        elif q_type == 'number':
            try:
                value = int(value)
            except:
                pass

    return value


def get_questions_from_submission(data):
    _data = {}
    prefix = 'questionnaire/q_'

    if isinstance(data, dict):
        for key, value in data.items():
            if key.startswith(prefix) and key.lstrip(prefix).isnumeric():
                q_num = key.lstrip(prefix)
                _data[q_num] = get_question_value(q_num, value)

    return _data


def process_questions(drupal, node, data):
    if isinstance(node, dict) and 'nid' and node:
        questions = {
            "qnid": node['nid']
        }
        questions["answers"] = get_questions_from_submission(data)

        if questions["answers"]:
            uri = drupal.get_uri(constants.QUESTIONNAIRE_SUBMIT_API_PATH)

            return drupal.post_data(uri, questions)

    return None


def parse_api_questions():
    drupal = Drupal(settings.DRUPAL_HOST)
    drupal.login(username=settings.DRUPAL_USERNAME,
                 password=settings.DRUPAL_PASSWORD)
    questions_path = 'api/views/api_questions.json'
    questions_uri = drupal.get_uri(questions_path)
    questions = drupal.get_node(questions_uri)

    for question in questions:
        title = question.get('title')
        taxonomy_vocabulary_1 = question.get('taxonomy_vocabulary_1')
        if isinstance(taxonomy_vocabulary_1, dict)\
                and 'und' in taxonomy_vocabulary_1:
            taxonomy_vocabulary_1 = taxonomy_vocabulary_1['und'][0]['tid']

        nid = question.get('nid')
        question_type = question.get('questionnaire_question_type')
        if isinstance(question_type, dict) and 'und' in question_type:
            question_type = question_type['und'][0]['value']

        options = question.get('questionnaire_question_options')
        option_str = ""
        if isinstance(options, dict) and 'und' in options:
            option_list = []

            for option in options["und"]:
                option_list.append('"%s"' % option["value"])

            option_str = ", ".join(option_list)

        subject = question.get("field_question_subject")["und"][0]["tid"]

        print(' %s, %s,%s,%s,"%s",%s' % (
            subject, nid, question_type, taxonomy_vocabulary_1, title,
            option_str))


if __name__ == '__main__':
    parse_api_questions()
