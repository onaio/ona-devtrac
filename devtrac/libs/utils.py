import json

from datetime import datetime

from devtrac.libs.devtrac.site_visit import (SiteVisitReport, RoadsideReport,
                                             HumanInterestReport)

SITE_VISIT_REPORT = '0'
ROAD_SIDE_REPORT = '1'
HUMAN_INTEREST_REPORT = '2'


def process_site_visit_submission(data):
    """Return a SiteVisit drupal node for processing with devtrac site"""

    field_place_lat_long = data.get('site_visit_group/s_field_place_lat_long')
    title = data.get('site_visit_group/site_visit_title')
    taxonomy_vocabulary_1 = data.get('site_visit_group/location_type')
    taxonomy_vocabulary_6 = data.get('site_visit_group/district')
    date_visited = data.get('site_visit_group/s_field_ftritem_date_visited')

    site_visit = SiteVisitReport(title)

    if isinstance(field_place_lat_long, str) and len(field_place_lat_long):
        if len(field_place_lat_long.split()) > 1:
            location = u' '.join(field_place_lat_long.split(' ')[:2])
            site_visit.set_location(location)

    if isinstance(date_visited, str):
        date_visited = datetime.strptime(date_visited, '%Y-%m-%d')
        site_visit.set_date_visited(date_visited.strftime('%d/%m/%Y'))

    site_visit.set_taxonomy_vocabulary(1, taxonomy_vocabulary_1)
    site_visit.set_taxonomy_vocabulary(6, taxonomy_vocabulary_6)
    site_visit.set_public_summary('n/a')
    site_visit.set_narrative('n/a')

    return site_visit


def process_road_side_submission(data):
    """Return a Road Side Report drupal node for processing with devtrac site
    """

    field_place_lat_long = data.get('roadside_group/field_ftritem_lat_long')
    title = data.get('roadside_group/roadside_title')
    taxonomy_vocabulary_6 = data.get('roadside_group/roadside_district')
    taxonomy_vocabulary_8 = data.get('roadside_group/sector')
    date_visited = data.get('roadside_group/field_ftritem_date_visited')
    public_summary = data.get('roadside_group/field_ftritem_public_summary')
    narrative = data.get('roadside_group/field_ftritem_narrative')

    site_visit = RoadsideReport(title)

    if isinstance(field_place_lat_long, str) and len(field_place_lat_long):
        if len(field_place_lat_long.split()) > 1:
            location = u' '.join(field_place_lat_long.split(' ')[:2])
            site_visit.set_location(location)

    if isinstance(date_visited, str):
        date_visited = datetime.strptime(date_visited, '%Y-%m-%d')
        site_visit.set_date_visited(date_visited.strftime('%d/%m/%Y'))

    if isinstance(taxonomy_vocabulary_8, str):
        taxonomy_vocabulary_8 = taxonomy_vocabulary_8.split(' ')

    site_visit.set_taxonomy_vocabulary(6, taxonomy_vocabulary_6)
    site_visit.set_taxonomy_vocabulary(8, taxonomy_vocabulary_8, multiple=True)
    site_visit.set_public_summary(public_summary)
    site_visit.set_narrative(narrative)

    return site_visit


def process_human_interest_submission(data):
    field_place_lat_long = data.get('human_interest/h_field_place_lat_long')
    title = data.get('human_interest/hi_title')
    taxonomy_vocabulary_1 = data.get('human_interest/hi_location_type')
    taxonomy_vocabulary_6 = data.get('human_interest/hi_district')
    date_visited = data.get('human_interest/hi_field_ftritem_date_visited')

    site_visit = HumanInterestReport(title)

    if isinstance(field_place_lat_long, str) and len(field_place_lat_long):
        if len(field_place_lat_long.split()) > 1:
            location = u' '.join(field_place_lat_long.split(' ')[:2])
            site_visit.set_location(location)

    if isinstance(date_visited, str):
        date_visited = datetime.strptime(date_visited, '%Y-%m-%d')
        site_visit.set_date_visited(date_visited.strftime('%d/%m/%Y'))

    site_visit.set_taxonomy_vocabulary(1, taxonomy_vocabulary_1)
    site_visit.set_taxonomy_vocabulary(6, taxonomy_vocabulary_6)
    site_visit.set_public_summary('n/a')
    site_visit.set_narrative('n/a')

    return site_visit


def process_json_submission(drupal, data, fieldtrip_id):
    """Receives a json string from an odk submission,
    then creates appropriate Site report
    """
    if isinstance(data, str):
        data = json.loads(data)

    if not isinstance(data, dict):
        raise Exception(u"Expecting dictionary for `data` parameter")

    node = None
    site_report_type = data.get('site_report_type')

    if site_report_type == SITE_VISIT_REPORT:
        node = process_site_visit_submission(data)
    elif site_report_type == ROAD_SIDE_REPORT:
        node = process_road_side_submission(data)
    elif site_report_type == HUMAN_INTEREST_REPORT:
        node = process_human_interest_submission(data)

    if node is not None:
        node.set_field_trip(fieldtrip_id)
        return drupal.create_node(node)

    return None
