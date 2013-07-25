# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'YearlyData'
        db.create_table(u'schools_yearlydata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('academic_year', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.AcademicYear'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.School'])),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('part_of_shift', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Cluster'], null=True, blank=True)),
            ('village', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Village'], null=True, blank=True)),
            ('ward_no', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('management', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.SchoolManaagement'], null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.SchoolCategory'], null=True, blank=True)),
            ('area_type', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('distance_from_brc', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('distance_from_crc', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('pre_primary_available', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('pre_primary_student_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pre_primary_teacher_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('residential', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('residential_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.ResidentialType'], null=True, blank=True)),
            ('lowest_class', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('highest_class', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'schools', ['YearlyData'])

        # Adding M2M table for field mediums on 'YearlyData'
        m2m_table_name = db.shorten_name(u'schools_yearlydata_mediums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('yearlydata', models.ForeignKey(orm[u'schools.yearlydata'], null=False)),
            ('instractionmedium', models.ForeignKey(orm[u'schools.instractionmedium'], null=False))
        ))
        db.create_unique(m2m_table_name, ['yearlydata_id', 'instractionmedium_id'])

        # Deleting field 'School.pre_primary_available'
        db.delete_column(u'schools_school', 'pre_primary_available')

        # Deleting field 'School.pre_primary_teacher_count'
        db.delete_column(u'schools_school', 'pre_primary_teacher_count')

        # Deleting field 'School.ward_no'
        db.delete_column(u'schools_school', 'ward_no')

        # Deleting field 'School.cluster'
        db.delete_column(u'schools_school', 'cluster_id')

        # Deleting field 'School.village'
        db.delete_column(u'schools_school', 'village_id')

        # Deleting field 'School.lowest_class'
        db.delete_column(u'schools_school', 'lowest_class')

        # Deleting field 'School.category'
        db.delete_column(u'schools_school', 'category_id')

        # Deleting field 'School.management'
        db.delete_column(u'schools_school', 'management_id')

        # Deleting field 'School.residential'
        db.delete_column(u'schools_school', 'residential')

        # Deleting field 'School.area_type'
        db.delete_column(u'schools_school', 'area_type')

        # Deleting field 'School.distance_from_brc'
        db.delete_column(u'schools_school', 'distance_from_brc')

        # Deleting field 'School.highest_class'
        db.delete_column(u'schools_school', 'highest_class')

        # Deleting field 'School.type'
        db.delete_column(u'schools_school', 'type')

        # Deleting field 'School.part_of_shift'
        db.delete_column(u'schools_school', 'part_of_shift')

        # Deleting field 'School.distance_from_crc'
        db.delete_column(u'schools_school', 'distance_from_crc')

        # Deleting field 'School.pre_primary_student_count'
        db.delete_column(u'schools_school', 'pre_primary_student_count')

        # Deleting field 'School.residential_type'
        db.delete_column(u'schools_school', 'residential_type_id')

        # Removing M2M table for field mediums on 'School'
        db.delete_table(db.shorten_name(u'schools_school_mediums'))


    def backwards(self, orm):
        # Deleting model 'YearlyData'
        db.delete_table(u'schools_yearlydata')

        # Removing M2M table for field mediums on 'YearlyData'
        db.delete_table(db.shorten_name(u'schools_yearlydata_mediums'))

        # Adding field 'School.pre_primary_available'
        db.add_column(u'schools_school', 'pre_primary_available',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.pre_primary_teacher_count'
        db.add_column(u'schools_school', 'pre_primary_teacher_count',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.ward_no'
        db.add_column(u'schools_school', 'ward_no',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.cluster'
        db.add_column(u'schools_school', 'cluster',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Cluster'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.village'
        db.add_column(u'schools_school', 'village',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Village'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.lowest_class'
        db.add_column(u'schools_school', 'lowest_class',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.category'
        db.add_column(u'schools_school', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.SchoolCategory'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.management'
        db.add_column(u'schools_school', 'management',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.SchoolManaagement'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.residential'
        db.add_column(u'schools_school', 'residential',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.area_type'
        db.add_column(u'schools_school', 'area_type',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.distance_from_brc'
        db.add_column(u'schools_school', 'distance_from_brc',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.highest_class'
        db.add_column(u'schools_school', 'highest_class',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.type'
        db.add_column(u'schools_school', 'type',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.part_of_shift'
        db.add_column(u'schools_school', 'part_of_shift',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.distance_from_crc'
        db.add_column(u'schools_school', 'distance_from_crc',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.pre_primary_student_count'
        db.add_column(u'schools_school', 'pre_primary_student_count',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'School.residential_type'
        db.add_column(u'schools_school', 'residential_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.ResidentialType'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field mediums on 'School'
        m2m_table_name = db.shorten_name(u'schools_school_mediums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('school', models.ForeignKey(orm[u'schools.school'], null=False)),
            ('instractionmedium', models.ForeignKey(orm[u'schools.instractionmedium'], null=False))
        ))
        db.create_unique(m2m_table_name, ['school_id', 'instractionmedium_id'])


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
        u'schools.academicyear': {
            'Meta': {'object_name': 'AcademicYear'},
            'from_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_year': ('django.db.models.fields.SmallIntegerField', [], {})
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
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pincode': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
        },
        u'schools.yearlydata': {
            'Meta': {'object_name': 'YearlyData'},
            'academic_year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.AcademicYear']"}),
            'area_type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.SchoolCategory']", 'null': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Cluster']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'distance_from_brc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'distance_from_crc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'highest_class': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowest_class': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'management': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.SchoolManaagement']", 'null': 'True', 'blank': 'True'}),
            'mediums': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['schools.InstractionMedium']", 'null': 'True', 'blank': 'True'}),
            'part_of_shift': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pre_primary_available': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pre_primary_student_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pre_primary_teacher_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'residential': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'residential_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.ResidentialType']", 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.School']"}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Village']", 'null': 'True', 'blank': 'True'}),
            'ward_no': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schools']