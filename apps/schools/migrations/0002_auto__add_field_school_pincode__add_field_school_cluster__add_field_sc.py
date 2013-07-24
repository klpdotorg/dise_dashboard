# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'School.pincode'
        db.add_column(u'schools_school', 'pincode',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.cluster'
        db.add_column(u'schools_school', 'cluster',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Cluster'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.village'
        db.add_column(u'schools_school', 'village',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Village'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'School.pincode'
        db.delete_column(u'schools_school', 'pincode')

        # Deleting field 'School.cluster'
        db.delete_column(u'schools_school', 'cluster_id')

        # Deleting field 'School.village'
        db.delete_column(u'schools_school', 'village_id')


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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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
        },
        u'schools.school': {
            'Meta': {'object_name': 'School'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Cluster']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pincode': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Village']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schools']