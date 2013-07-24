# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cluster.block'
        db.add_column(u'common_cluster', 'block',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Block'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Block.education_district'
        db.add_column(u'common_block', 'education_district',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.EducationDistrict'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'EducationDistrict.state'
        db.add_column(u'common_educationdistrict', 'state',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.State'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cluster.block'
        db.delete_column(u'common_cluster', 'block_id')

        # Deleting field 'Block.education_district'
        db.delete_column(u'common_block', 'education_district_id')

        # Deleting field 'EducationDistrict.state'
        db.delete_column(u'common_educationdistrict', 'state_id')


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
        }
    }

    complete_apps = ['common']