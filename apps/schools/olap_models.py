# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils import simplejson as json
from django.core import serializers


class BasicData(models.Model):
    school_code = models.BigIntegerField(primary_key=True)
    centroid = models.GeometryField(blank=True, null=True)
    district = models.CharField(max_length=50, blank=True)
    school_name = models.CharField(max_length=200, blank=True)
    block_name = models.CharField(max_length=50, blank=True)
    cluster_name = models.CharField(max_length=50, blank=True)
    village_name = models.CharField(max_length=50, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    rural_urban = models.IntegerField(null=True, blank=True)
    medium_of_instruction = models.IntegerField(null=True, blank=True)
    distance_brc = models.FloatField(null=True, blank=True)
    distance_crc = models.FloatField(null=True, blank=True)
    yeur_estd = models.IntegerField(null=True, blank=True)
    pre_pry_yn = models.IntegerField(null=True, blank=True)
    residential_sch_yn = models.IntegerField(null=True, blank=True)
    sch_management = models.IntegerField(null=True, blank=True)
    lowest_class = models.IntegerField(null=True, blank=True)
    highest_class = models.IntegerField(null=True, blank=True)
    sch_category = models.IntegerField(null=True, blank=True)
    pre_pry_students = models.IntegerField(null=True, blank=True)
    school_type = models.IntegerField(null=True, blank=True)
    shift_school_yn = models.IntegerField(null=True, blank=True)
    no_of_working_days = models.IntegerField(null=True, blank=True)
    no_of_acad_inspection = models.IntegerField(null=True, blank=True)
    residential_sch_type = models.IntegerField(null=True, blank=True)
    pre_pry_teachers = models.IntegerField(null=True, blank=True)
    visits_by_brc = models.IntegerField(null=True, blank=True)
    visits_by_crc = models.IntegerField(null=True, blank=True)
    school_dev_grant_recd = models.FloatField(null=True, blank=True)
    school_dev_grant_expnd = models.FloatField(null=True, blank=True)
    tlm_grant_recd = models.FloatField(null=True, blank=True)
    tlm_grant_expnd = models.FloatField(null=True, blank=True)
    funds_from_students_recd = models.FloatField(null=True, blank=True)
    funds_from_students_expnd = models.FloatField(null=True, blank=True)
    building_status = models.IntegerField(null=True, blank=True)
    tot_clrooms = models.IntegerField(null=True, blank=True)
    classrooms_in_good_condition = models.IntegerField(null=True, blank=True)
    classrooms_require_major_repair = models.IntegerField(null=True, blank=True)
    classrooms_require_minor_repair = models.IntegerField(null=True, blank=True)
    other_rooms_in_good_cond = models.IntegerField(null=True, blank=True)
    other_rooms_need_major_rep = models.IntegerField(null=True, blank=True)
    other_rooms_need_minor_rep = models.IntegerField(null=True, blank=True)
    toilet_common = models.IntegerField(null=True, blank=True)
    toilet_boys = models.IntegerField(null=True, blank=True)
    toilet_girls = models.IntegerField(null=True, blank=True)
    kitchen_devices_grant = models.IntegerField(null=True, blank=True)
    status_of_mdm = models.IntegerField(null=True, blank=True)
    computer_aided_learnin_lab = models.IntegerField(null=True, blank=True)
    separate_room_for_headmaster = models.IntegerField(null=True, blank=True)
    electricity = models.IntegerField(null=True, blank=True)
    boundary_wall = models.IntegerField(null=True, blank=True)
    library_yn = models.IntegerField(null=True, blank=True)
    playground = models.IntegerField(null=True, blank=True)
    blackboard = models.IntegerField(null=True, blank=True)
    books_in_library = models.IntegerField(null=True, blank=True)
    drinking_water = models.IntegerField(null=True, blank=True)
    medical_checkup = models.IntegerField(null=True, blank=True)
    ramps = models.IntegerField(null=True, blank=True)
    no_of_computers = models.IntegerField(null=True, blank=True)
    male_tch = models.IntegerField(null=True, blank=True)
    female_tch = models.IntegerField(null=True, blank=True)
    noresp_tch = models.IntegerField(null=True, blank=True)
    head_teacher = models.IntegerField(null=True, blank=True)
    graduate_teachers = models.IntegerField(null=True, blank=True)
    tch_with_professional_qualification = models.IntegerField(null=True, blank=True)
    days_involved_in_non_tch_assgn = models.IntegerField(null=True, blank=True)
    teachers_involved_in_non_tch_assgn = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class Dise1011BasicData(BasicData):
    class Meta:
        db_table = 'dise_1011_basic_data'


class Dise1112BasicData(BasicData):
    class Meta:
        db_table = 'dise_1112_basic_data'


yearly_data = {
    '10-11': Dise1011BasicData,
    '11-12': Dise1112BasicData
}


class BaseEntity:
    @classmethod
    def to_json_str(cls, d=dict()):
        return json.dumps(d)


class School(BaseEntity):
    @classmethod
    def getInfo(cls, params):
        code = params.get('code', -1)
        result = dict()
        result['query'] = params

        try:
            yearly_data_model = yearly_data.get(params.get('session', '10-11'))
            school = yearly_data_model.objects.extra(
                select={
                    'centroid': 'ST_AsText("dise_1011_basic_data"."centroid")'
                }
            ).values(
                'school_code', 'school_name', 'cluster_name', 'block_name', 'centroid'
            ).get(school_code=code)

            result['school'] = school
        except (yearly_data_model.DoesNotExist, Exception) as e:
            result['error'] = str(e)

        return cls.to_json_str(result)

    @classmethod
    def search(cls, params):
        result = dict()
        result['query'] = params
        yearly_data_model = yearly_data.get(params.get('session', '10-11'))

        if len(params.keys()) > 1:
            schools = yearly_data_model.objects.extra(
                select={
                    'centroid': 'ST_AsText("dise_1011_basic_data"."centroid")'
                }
            ).values(
                'school_code', 'school_name', 'cluster_name', 'block_name', 'centroid'
            )

        if 'name' in params and params.get('name', ''):
            schools = schools.filter(school_name__icontains=params.get('name'))

        if 'cluster' in params and params.get('cluster', ''):
            schools = schools.filter(cluster_name__icontains=params.get('cluster'))

        if params.get('geo') == 'true':
            schools = schools.filter(centroid__isnull=False)
        elif params.get('geo') == 'false':
            schools = schools.filter(centroid__isnull=True)

        if 'limit' in params and params.get('limit', 0):
            schools = schools[:params.get('limit')]

        result['schools'] = list(schools)
        return cls.to_json_str(result)


class Cluster(BaseEntity):
    @classmethod
    def search(cls, params):
        result = dict()
        result['query'] = params
        yearly_data_model = yearly_data.get(params.get('session', '10-11'))

        if len(params.keys()) > 1:
            clusters = yearly_data_model.objects.values(
                'cluster_name', 'block_name', 'village_name', 'district'
            ).distinct('cluster_name')

        if 'name' in params and params.get('name', ''):
            clusters = clusters.filter(cluster_name__icontains=params.get('name'))

        if 'block' in params and params.get('block', ''):
            clusters = clusters.filter(block_name__icontains=params.get('block'))

        result['clusters'] = list(clusters)
        return cls.to_json_str(result)
