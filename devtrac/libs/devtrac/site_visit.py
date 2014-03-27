from devtrac.libs.drupal import DrupalNode


class SiteVisit(DrupalNode):
    node_type = u'ftritem'
    taxonomy_vocabulary_7 = 209

    def __init__(self, title, **kwargs):
        if kwargs.get('node_type'):
            del kwargs['node_type']

        super(SiteVisit, self).__init__(title, self.node_type, **kwargs)

        self.set_taxonomy_vocabulary(7, self.taxonomy_vocabulary_7)

    def set_date_visited(self, date_visited):
        self._node_dict.update(
            {
                'field_ftritem_date_visited':
                {
                    'und': [{
                        'value': {'date': date_visited}
                    }]
                }
            }
        )

    def set_narrative(self, narrative):
        self._node_dict.update(
            {
                'field_ftritem_narrative': {
                    'und': [
                        {'value': narrative}
                    ]
                }
            }
        )

    def set_und(self, field, value):
        self._node_dict.update(
            {
                field: {
                    'und': [
                        {'value': value}
                    ]
                }
            }
        )

    def set_public_summary(self, summary):
        self._node_dict.update(
            {
                'field_ftritem_public_summary': {
                    'und': [
                        {'value': summary}
                    ]
                }
            }
        )

    def set_target_id(self, field, target):
        self._node_dict.update({
            field: {
                'und': [{'target_id': target}]
            }
        })

    def set_field_trip(self, field_trip_id):
        self.set_target_id('field_ftritem_field_trip', field_trip_id)

    def set_place(self, place):
        if place is not None:
            self.set_target_id('field_ftritem_place', place)

    def set_location(self, location):
        if location is not None:
            self._node_dict.update({'field_ftritem_lat_long': {
                'und': [{'value': {'wkt': 'POINT (%s)' % location}}]
            }})

    def set_site_visit(self, date_visited, location_type, narrative, summary,
                       field_trip_id=None, location=None, place=None):
        self.set_date_visited(date_visited)
        self.set_taxonomy_vocabulary(1, location_type)
        self.set_narrative(narrative)
        self.set_public_summary(summary)
        self.set_location(location)
        self.set_place(place)
        # self.set_und('field_ftritem_status', 'Submitted')

        if field_trip_id:
            self.set_field_trip(field_trip_id)
