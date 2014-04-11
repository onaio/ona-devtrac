# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Submission'
        db.create_table('main_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('jsonfield.fields.JSONField')()),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('main', ['Submission'])


    def backwards(self, orm):
        # Deleting model 'Submission'
        db.delete_table('main_submission')


    models = {
        'main.submission': {
            'Meta': {'object_name': 'Submission'},
            'data': ('jsonfield.fields.JSONField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['main']