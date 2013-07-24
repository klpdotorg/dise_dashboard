# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Cluster', fields ['name']
        db.delete_unique(u'common_cluster', ['name'])


    def backwards(self, orm):
        # Adding unique constraint on 'Cluster', fields ['name']
        db.create_unique(u'common_cluster', ['name'])


    models = {
        u'common.block': {
            'Meta': {'object_name': 'Block'},
            'education_district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.EducationDistrict']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'common.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Block']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'common.educationdistrict': {
            'Meta': {'object_name': 'EducationDistrict'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.State']", 'null': 'True', 'blank': 'True'})
        },
        u'common.state': {
            'Meta': {'object_name': 'State'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'common.village': {
            'Meta': {'object_name': 'Village'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['common']