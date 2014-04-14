from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField


class Submission(models.Model):
    data = JSONField()
    processed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def processed_string(self):
        return _(u"Yes") if self.processed else _(u"No")
