import json

from datetime import datetime

from devtrac.libs.devtrac.site_visit import SiteReport

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


def process_site_report_submission(data, date_visited=None):
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

    return site_report


def process_json_submission(drupal, data, date_visited=None):
    """Receives a json string from an odk submission,
    then creates appropriate Site report
    """
    if isinstance(data, str):
        data = json.loads(data)

    if not isinstance(data, dict):
        raise Exception(u"Expecting dictionary for `data` parameter")

    node = process_site_report_submission(data, date_visited)

    if node is not None:
        return drupal.create_node(node)

    return None
