# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cluster'
        db.create_table(u'common_cluster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'common', ['Cluster'])

        # Adding model 'Block'
        db.create_table(u'common_block', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'common', ['Block'])

        # Adding model 'EducationDistrict'
        db.create_table(u'common_educationdistrict', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'common', ['EducationDistrict'])

        # Adding model 'Village'
        db.create_table(u'common_village', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'common', ['Village'])

        # Adding model 'State'
        db.create_table(u'common_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'common', ['State'])


    def backwards(self, orm):
        # Deleting model 'Cluster'
        db.delete_table(u'common_cluster')

        # Deleting model 'Block'
        db.delete_table(u'common_block')

        # Deleting model 'EducationDistrict'
        db.delete_table(u'common_educationdistrict')

        # Deleting model 'Village'
        db.delete_table(u'common_village')

        # Deleting model 'State'
        db.delete_table(u'common_state')


    models = {
        u'common.block': {
            'Meta': {'object_name': 'Block'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'common.cluster': {
            'Meta': {'object_name': 'Cluster'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'common.educationdistrict': {
            'Meta': {'object_name': 'EducationDistrict'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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