from devtrac.libs.drupal import DrupalNode


class FieldTrip(DrupalNode):
    """Class to represent a FieldTrip Node"""

    PROGRAMME_OVERSIGHT = 236
    ADVISORY_TECHNICAL_ASSISTANCE = 237
    REPRESENTATIONAL = 238
    TRAIN_FACILITATE_CONVENE_MEETING = 239
    PARTICIPATION_IN_MEETING = 240
    HACT_ACTIVITIES = 834
    PROGRAMME_QUALITY_ASSURANCE_VISIT = 835
    EMERGENCY_PREPAREDNESS_AND_RESPONSE = 836
    DONOR_VISIT = 837
    SUPPLY_MONITORING = 838
    DOCUMENTATION_AND_VISIBILITY = 839
    DCT_MONITORING = 840
    FAMILY_HEALTH_DAYS = 841
    OTHER = 241

    FIELD_TRIP_PURPOSE = {
        PROGRAMME_OVERSIGHT: u"Programme Oversight",
        ADVISORY_TECHNICAL_ASSISTANCE: u"Advisory/Technical Assistance",
        REPRESENTATIONAL: u"Representational",
        TRAIN_FACILITATE_CONVENE_MEETING: u"Train/Facilitate/Convene Meeting",
        PARTICIPATION_IN_MEETING: u"Participation in Meeting",
        HACT_ACTIVITIES: u"HACT Activities",
        PROGRAMME_QUALITY_ASSURANCE_VISIT:
        u"Programme Quality Assurance Visit",
        EMERGENCY_PREPAREDNESS_AND_RESPONSE:
        u"Emergency Preparedness and Response",
        DONOR_VISIT: u"Donor Visit",
        SUPPLY_MONITORING: u"Supply Monitoring",
        DOCUMENTATION_AND_VISIBILITY: u"Documentation and Visibility",
        DCT_MONITORING: u"DCT Monitoring",
        FAMILY_HEALTH_DAYS: u"Family Health Days",
        OTHER: u"Other"
    }
    node_type = u'fieldtrip'

    def __init__(self, title, **kwargs):
        if kwargs.get('node_type'):
            del kwargs['node_type']

        super(FieldTrip, self).__init__(title, self.node_type, **kwargs)

    def add_trip_purpose(self, purpose, percentage):
        """Add Field Trip Purpose"""
        self._node_dict.update({
            'field_fieldtrip_fc_purpose': {
                'und': [{
                    'field_fieldtrip_purpose_percent': {
                        'und': [{
                            'value': percentage
                        }]},
                    'field_fieldtrip_fc_purpose_purps': {'und': purpose}
                }]
            }
        })

    def add_administrative_boundary(self, location):
        self._node_dict.update({
            'taxonomy_vocabulary_6': {'und': [{'value': location}]}
        })
