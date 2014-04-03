from django.db import models
from jsonfield import JSONField


class Submission(models.Model):
    data = JSONField()
    processed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
