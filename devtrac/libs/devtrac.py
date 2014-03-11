from devtrac.libs.drupal import DrupalNode


class FieldTrip(DrupalNode):
    """Class to represent a FieldTrip Node"""

    node_type = u'fieldtrip'

    def __init__(self, title, **kwargs):
        if not isinstance(title, str):
            raise Exception(u"Expected a string for title")

        if kwargs.get('node_type'):
            del kwargs['node_type']

        super(FieldTrip, self).__init__(title, self.node_type, **kwargs)
