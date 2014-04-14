# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Submission.nid'
        db.add_column('main_submission', 'nid',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Submission.uri'
        db.add_column('main_submission', 'uri',
                      self.gf('django.db.models.fields.CharField')(null=True, max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Submission.nid'
        db.delete_column('main_submission', 'nid')

        # Deleting field 'Submission.uri'
        db.delete_column('main_submission', 'uri')


    models = {
        'main.submission': {
            'Meta': {'object_name': 'Submission'},
            'data': ('jsonfield.fields.JSONField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'nid': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uri': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['main']