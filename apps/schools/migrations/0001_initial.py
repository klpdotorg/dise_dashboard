# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'School'
        db.create_table(u'schools_school', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'schools', ['School'])


    def backwards(self, orm):
        # Deleting model 'School'
        db.delete_table(u'schools_school')


    models = {
        u'schools.school': {
            'Meta': {'object_name': 'School'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['schools']