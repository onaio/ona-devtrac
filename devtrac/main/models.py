from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField


class Submission(models.Model):
    # ona form submission json
    data = JSONField()

    # sent to devtrac successfully
    processed = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # Drupla Node ID
    nid = models.PositiveIntegerField(null=True, blank=True)

    # Drupal Node URI
    uri = models.CharField(max_length=255, null=True, blank=True)

    def processed_string(self):
        return _(u"Yes") if self.processed else _(u"No")
