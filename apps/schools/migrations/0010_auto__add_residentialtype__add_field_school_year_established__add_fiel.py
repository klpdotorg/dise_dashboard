# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResidentialType'
        db.create_table(u'schools_residentialtype', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'schools', ['ResidentialType'])

        # Adding field 'School.year_established'
        db.add_column(u'schools_school', 'year_established',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.management'
        db.add_column(u'schools_school', 'management',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.SchoolManaagement'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.category'
        db.add_column(u'schools_school', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.SchoolCategory'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.medium'
        db.add_column(u'schools_school', 'medium',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.InstractionMedium'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.distance_from_brc'
        db.add_column(u'schools_school', 'distance_from_brc',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.distance_from_crc'
        db.add_column(u'schools_school', 'distance_from_crc',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.pre_primary_available'
        db.add_column(u'schools_school', 'pre_primary_available',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.pre_primary_student_count'
        db.add_column(u'schools_school', 'pre_primary_student_count',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.pre_primary_teacher_count'
        db.add_column(u'schools_school', 'pre_primary_teacher_count',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.residential'
        db.add_column(u'schools_school', 'residential',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.residential_type'
        db.add_column(u'schools_school', 'residential_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.ResidentialType'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.lowest_class'
        db.add_column(u'schools_school', 'lowest_class',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.highest_class'
        db.add_column(u'schools_school', 'highest_class',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ResidentialType'
        db.delete_table(u'schools_residentialtype')

        # Deleting field 'School.year_established'
        db.delete_column(u'schools_school', 'year_established')

        # Deleting field 'School.management'
        db.delete_column(u'schools_school', 'management_id')

        # Deleting field 'School.category'
        db.delete_column(u'schools_school', 'category_id')

        # Deleting field 'School.medium'
        db.delete_column(u'schools_school', 'medium_id')

        # Deleting field 'School.distance_from_brc'
        db.delete_column(u'schools_school', 'distance_from_brc')

        # Deleting field 'School.distance_from_crc'
        db.delete_column(u'schools_school', 'distance_from_crc')

        # Deleting field 'School.pre_primary_available'
        db.delete_column(u'schools_school', 'pre_primary_available')

        # Deleting field 'School.pre_primary_student_count'
        db.delete_column(u'schools_school', 'pre_primary_student_count')

        # Deleting field 'School.pre_primary_teacher_count'
        db.delete_column(u'schools_school', 'pre_primary_teacher_count')

        # Deleting field 'School.residential'
        db.delete_column(u'schools_school', 'residential')

        # Deleting field 'School.residential_type'
        db.delete_column(u'schools_school', 'residential_type_id')

        # Deleting field 'School.lowest_class'
        db.delete_column(u'schools_school', 'lowest_class')

        # Deleting field 'School.highest_class'
        db.delete_column(u'schools_school', 'highest_class')


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
            'Meta': {'ordering': "('name',)", 'object_name': 'Village'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'schools.instractionmedium': {
            'Meta': {'object_name': 'InstractionMedium'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'schools.residentialtype': {
            'Meta': {'object_name': 'ResidentialType'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'schools.school': {
            'Meta': {'object_name': 'School'},
            'area_type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.SchoolCategory']", 'null': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Cluster']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'distance_from_brc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'distance_from_crc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'highest_class': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowest_class': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'management': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.SchoolManaagement']", 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.InstractionMedium']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pincode': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pre_primary_available': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pre_primary_student_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pre_primary_teacher_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'residential': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'residential_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.ResidentialType']", 'null': 'True', 'blank': 'True'}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Village']", 'null': 'True', 'blank': 'True'}),
            'ward_no': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'year_established': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'schools.schoolcategory': {
            'Meta': {'object_name': 'SchoolCategory'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'schools.schoolmanaagement': {
            'Meta': {'object_name': 'SchoolManaagement'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['schools']