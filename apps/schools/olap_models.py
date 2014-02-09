# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from common.models import search_choices, YESNO, AREA, SCHOOL_CATEGORY, SCHOOL_MANAGEMENT, SCHOOL_TYPES, MEDIUM, MDM_STATUS, KITCHENSHED_STATUS, BOUNDARY_WALL

from django.contrib.gis.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True


class BasicData(BaseModel):
    school_code = models.BigIntegerField(primary_key=True)
    centroid = models.GeometryField(blank=True, null=True)
    district = models.CharField(max_length=50, blank=True)
    school_name = models.CharField(max_length=200, blank=True)
    block_name = models.CharField(max_length=50, blank=True)
    cluster_name = models.CharField(max_length=50, blank=True)
    village_name = models.CharField(max_length=50, blank=True)
    assembly_name = models.CharField(max_length=35, blank=True)
    parliament_name = models.CharField(max_length=35, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    rural_urban = models.IntegerField(choices=AREA, null=True, blank=True)
    medium_of_instruction = models.IntegerField(choices=MEDIUM, null=True, blank=True)
    distance_brc = models.FloatField(null=True, blank=True)
    distance_crc = models.FloatField(null=True, blank=True)
    yeur_estd = models.IntegerField(null=True, blank=True)
    pre_pry_yn = models.IntegerField(null=True, blank=True)
    residential_sch_yn = models.IntegerField(null=True, blank=True)
    sch_management = models.IntegerField(choices=SCHOOL_MANAGEMENT, null=True, blank=True)
    lowest_class = models.IntegerField(null=True, blank=True)
    highest_class = models.IntegerField(null=True, blank=True)
    sch_category = models.IntegerField(choices=SCHOOL_CATEGORY, null=True, blank=True)
    pre_pry_students = models.IntegerField(null=True, blank=True)
    school_type = models.IntegerField(choices=SCHOOL_TYPES, null=True, blank=True)
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
    classrooms_require_major_repair = models.IntegerField(choices=YESNO, null=True, blank=True)
    classrooms_require_minor_repair = models.IntegerField(choices=YESNO, null=True, blank=True)
    other_rooms_in_good_cond = models.IntegerField(null=True, blank=True)
    other_rooms_need_major_rep = models.IntegerField(null=True, blank=True)
    other_rooms_need_minor_rep = models.IntegerField(null=True, blank=True)
    toilet_common = models.IntegerField(null=True, blank=True)
    toilet_boys = models.IntegerField(null=True, blank=True)
    toilet_girls = models.IntegerField(null=True, blank=True)
    kitchen_devices_grant = models.IntegerField(null=True, blank=True)
    status_of_mdm = models.IntegerField(choices=MDM_STATUS, null=True, blank=True)
    computer_aided_learnin_lab = models.IntegerField(null=True, blank=True)
    separate_room_for_headmaster = models.IntegerField(null=True, blank=True)
    electricity = models.IntegerField(choices=YESNO, null=True, blank=True)
    boundary_wall = models.IntegerField(choices=BOUNDARY_WALL, null=True, blank=True)
    library_yn = models.IntegerField(choices=YESNO, null=True, blank=True)
    playground = models.IntegerField(null=True, blank=True)
    blackboard = models.IntegerField(null=True, blank=True)
    books_in_library = models.IntegerField(null=True, blank=True)
    drinking_water = models.IntegerField(null=True, blank=True)
    medical_checkup = models.IntegerField(null=True, blank=True)
    ramps = models.IntegerField(choices=YESNO, null=True, blank=True)
    no_of_computers = models.IntegerField(null=True, blank=True)
    male_tch = models.IntegerField(null=True, blank=True)
    female_tch = models.IntegerField(null=True, blank=True)
    noresp_tch = models.IntegerField(null=True, blank=True)
    head_teacher = models.IntegerField(null=True, blank=True)
    graduate_teachers = models.IntegerField(null=True, blank=True)
    tch_with_professional_qualification = models.IntegerField(null=True, blank=True)
    days_involved_in_non_tch_assgn = models.IntegerField(null=True, blank=True)
    teachers_involved_in_non_tch_assgn = models.IntegerField(null=True, blank=True)
    class1_total_enr_boys = models.IntegerField(blank=True, null=True)
    class2_total_enr_boys = models.IntegerField(blank=True, null=True)
    class3_total_enr_boys = models.IntegerField(blank=True, null=True)
    class4_total_enr_boys = models.IntegerField(blank=True, null=True)
    class5_total_enr_boys = models.IntegerField(blank=True, null=True)
    class6_total_enr_boys = models.IntegerField(blank=True, null=True)
    class7_total_enr_boys = models.IntegerField(blank=True, null=True)
    class8_total_enr_boys = models.IntegerField(blank=True, null=True)
    class1_total_enr_girls = models.IntegerField(blank=True, null=True)
    class2_total_enr_girls = models.IntegerField(blank=True, null=True)
    class3_total_enr_girls = models.IntegerField(blank=True, null=True)
    class4_total_enr_girls = models.IntegerField(blank=True, null=True)
    class5_total_enr_girls = models.IntegerField(blank=True, null=True)
    class6_total_enr_girls = models.IntegerField(blank=True, null=True)
    class7_total_enr_girls = models.IntegerField(blank=True, null=True)
    class8_total_enr_girls = models.IntegerField(blank=True, null=True)
    total_boys = models.IntegerField(blank=True, null=True)
    total_girls = models.IntegerField(blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True


class AggregationBase(models.Model):
    sum_schools = models.BigIntegerField(null=True, blank=True)
    sum_rural_schools = models.BigIntegerField(null=True, blank=True)
    avg_distance_brc = models.FloatField(null=True, blank=True)
    avg_distance_crc = models.FloatField(null=True, blank=True)
    sum_pre_primary_schools = models.BigIntegerField(null=True, blank=True)
    sum_residential_schools = models.BigIntegerField(null=True, blank=True)
    sum_pre_primary_students = models.BigIntegerField(null=True, blank=True)
    avg_pre_primary_students = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_shift_schools = models.BigIntegerField(null=True, blank=True)
    sum_no_of_working_days = models.BigIntegerField(null=True, blank=True)
    avg_no_of_working_days = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_no_of_acad_inspection = models.BigIntegerField(null=True, blank=True)
    avg_no_of_acad_inspection = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_visits_by_brc = models.BigIntegerField(null=True, blank=True)
    avg_visits_by_brc = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_visits_by_crc = models.BigIntegerField(null=True, blank=True)
    avg_visits_by_crc = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_school_dev_grant_recd = models.FloatField(null=True, blank=True)
    avg_school_dev_grant_recd = models.FloatField(null=True, blank=True)
    sum_school_dev_grant_expnd = models.FloatField(null=True, blank=True)
    avg_school_dev_grant_expnd = models.FloatField(null=True, blank=True)
    sum_tlm_grant_recd = models.FloatField(null=True, blank=True)
    avg_tlm_grant_recd = models.FloatField(null=True, blank=True)
    sum_tlm_grant_expnd = models.FloatField(null=True, blank=True)
    avg_tlm_grant_expnd = models.FloatField(null=True, blank=True)
    sum_funds_from_students_recd = models.FloatField(null=True, blank=True)
    avg_funds_from_students_recd = models.FloatField(null=True, blank=True)
    sum_funds_from_students_expnd = models.FloatField(null=True, blank=True)
    avg_funds_from_students_expnd = models.FloatField(null=True, blank=True)
    sum_tot_clrooms = models.BigIntegerField(null=True, blank=True)
    avg_tot_clrooms = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_classrooms_in_good_condition = models.BigIntegerField(null=True, blank=True)
    avg_classrooms_in_good_condition = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_classrooms_require_major_repair = models.BigIntegerField(null=True, blank=True)
    avg_classrooms_require_major_repair = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_classrooms_require_minor_repair = models.BigIntegerField(null=True, blank=True)
    avg_classrooms_require_minor_repair = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_other_rooms_in_good_cond = models.BigIntegerField(null=True, blank=True)
    avg_other_rooms_in_good_cond = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_other_rooms_need_major_rep = models.BigIntegerField(null=True, blank=True)
    avg_other_rooms_need_major_rep = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_other_rooms_need_minor_rep = models.BigIntegerField(null=True, blank=True)
    avg_other_rooms_need_minor_rep = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_toilet_common = models.BigIntegerField(null=True, blank=True)
    avg_toilet_common = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_toilet_boys = models.BigIntegerField(null=True, blank=True)
    avg_toilet_boys = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_toilet_girls = models.BigIntegerField(null=True, blank=True)
    avg_toilet_girls = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_kitchen_devices_grant = models.BigIntegerField(null=True, blank=True)
    avg_kitchen_devices_grant = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_has_mdm = models.BigIntegerField(null=True, blank=True)
    sum_has_cal_lab = models.BigIntegerField(null=True, blank=True)
    sum_has_separate_room_for_headmaster = models.BigIntegerField(null=True, blank=True)
    sum_has_electricity = models.BigIntegerField(null=True, blank=True)
    sum_has_boundary_wall = models.BigIntegerField(null=True, blank=True)
    sum_has_library = models.BigIntegerField(null=True, blank=True)
    sum_books_in_library = models.BigIntegerField(null=True, blank=True)
    avg_books_in_library = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_has_playground = models.BigIntegerField(null=True, blank=True)
    sum_has_blackboard = models.BigIntegerField(null=True, blank=True)
    sum_has_drinking_water = models.BigIntegerField(null=True, blank=True)
    sum_has_medical_checkup = models.BigIntegerField(null=True, blank=True)
    sum_has_ramps = models.BigIntegerField(null=True, blank=True)
    sum_no_of_computers = models.BigIntegerField(null=True, blank=True)
    avg_no_of_computers = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_male_tch = models.BigIntegerField(null=True, blank=True)
    avg_male_tch = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_female_tch = models.BigIntegerField(null=True, blank=True)
    avg_female_tch = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_noresp_tch = models.BigIntegerField(null=True, blank=True)
    avg_noresp_tch = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_head_teacher = models.BigIntegerField(null=True, blank=True)
    avg_head_teacher = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_graduate_teachers = models.BigIntegerField(null=True, blank=True)
    avg_graduate_teachers = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_tch_with_professional_qualification = models.BigIntegerField(null=True, blank=True)
    avg_tch_with_professional_qualification = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_days_involved_in_non_tch_assgn = models.BigIntegerField(null=True, blank=True)
    avg_days_involved_in_non_tch_assgn = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_teachers_involved_in_non_tch_assgn = models.BigIntegerField(null=True, blank=True)
    avg_teachers_involved_in_non_tch_assgn = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    sum_boys = models.BigIntegerField(blank=True, null=True)
    avg_boys = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sum_girls = models.BigIntegerField(blank=True, null=True)
    avg_girls = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        abstract = True


class AssemblyAggregations(BaseModel, AggregationBase):
    assembly_name = models.CharField(max_length=35, primary_key=True)
    centroid = models.GeometryField(blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True


class BlockAggregations(BaseModel, AggregationBase):
    block_name = models.CharField(max_length=50, primary_key=True)
    district = models.CharField(max_length=50, blank=True)
    centroid = models.GeometryField(blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True


class ClusterAggregations(BaseModel, AggregationBase):
    cluster_name = models.CharField(max_length=50, primary_key=True)
    block_name = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)

    centroid = models.PointField(blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True
        unique_together = ("cluster_name", "block_name")


class ParliamentAggregations(BaseModel, AggregationBase):
    parliament_name = models.CharField(max_length=35, primary_key=True)


    objects = models.GeoManager()

    class Meta:
        abstract = True

class DistrictAggregations(BaseModel, AggregationBase):
    district = models.CharField(max_length=35, primary_key=True)
    centroid = models.GeometryField(blank=True, null=True)


    objects = models.GeoManager()

    class Meta:
        abstract = True


class PincodeAggregations(BaseModel, AggregationBase):
    pincode = models.IntegerField(blank=True, primary_key=True)
    centroid = models.PointField(blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True


class Dise1011AssemblyAggregations(AssemblyAggregations):
    class Meta:
        db_table = 'dise_1011_assembly_aggregations'


class Dise1112AssemblyAggregations(AssemblyAggregations):
    class Meta:
        db_table = 'dise_1112_assembly_aggregations'


class Dise1213AssemblyAggregations(AssemblyAggregations):
    class Meta:
        db_table = 'dise_1213_assembly_aggregations'


class Dise1011BlockAggregations(BlockAggregations):
    class Meta:
        db_table = 'dise_1011_block_aggregations'


class Dise1112BlockAggregations(BlockAggregations):
    class Meta:
        db_table = 'dise_1112_block_aggregations'


class Dise1213BlockAggregations(BlockAggregations):
    class Meta:
        db_table = 'dise_1213_block_aggregations'


class Dise1011ClusterAggregations(ClusterAggregations):
    class Meta:
        db_table = 'dise_1011_cluster_aggregations'


class Dise1112ClusterAggregations(ClusterAggregations):
    class Meta:
        db_table = 'dise_1112_cluster_aggregations'


class Dise1213ClusterAggregations(ClusterAggregations):
    class Meta:
        db_table = 'dise_1213_cluster_aggregations'


class Dise1011ParliamentAggregations(ParliamentAggregations):
    class Meta:
        db_table = 'dise_1011_parliament_aggregations'


class Dise1112ParliamentAggregations(ParliamentAggregations):
    class Meta:
        db_table = 'dise_1112_parliament_aggregations'


class Dise1213ParliamentAggregations(ParliamentAggregations):
    class Meta:
        db_table = 'dise_1213_parliament_aggregations'


class Dise1011DistrictAggregations(DistrictAggregations):
    class Meta:
        db_table = 'dise_1011_district_aggregations'


class Dise1112DistrictAggregations(DistrictAggregations):
    class Meta:
        db_table = 'dise_1112_district_aggregations'


class Dise1213DistrictAggregations(DistrictAggregations):
    class Meta:
        db_table = 'dise_1213_district_aggregations'


class Dise1011PincodeAggregations(PincodeAggregations):
    class Meta:
        db_table = 'dise_1011_pincode_aggregations'


class Dise1112PincodeAggregations(PincodeAggregations):
    class Meta:
        db_table = 'dise_1112_pincode_aggregations'


class Dise1213PincodeAggregations(PincodeAggregations):
    class Meta:
        db_table = 'dise_1213_pincode_aggregations'


class Dise1011BasicData(BasicData):
    class Meta:
        db_table = 'dise_1011_basic_data'


class Dise1112BasicData(BasicData):
    class Meta:
        db_table = 'dise_1112_basic_data'


class Dise1213BasicData(BasicData):
    class Meta:
        db_table = 'dise_1213_basic_data'


def get_models(session='10-11', what='all'):
    session = session.replace('-', '')

    school_model = globals().get('Dise{}BasicData'.format(session))
    if what == 'school':
        return school_model

    cluster_model = globals().get('Dise{}ClusterAggregations'.format(session))
    if what == 'cluster':
        return cluster_model

    block_model = globals().get('Dise{}BlockAggregations'.format(session))
    if what == 'block':
        return block_model

    district_model = globals().get('Dise{}DistrictAggregations'.format(session))
    if what == 'district':
        return district_model

    pincode_model = globals().get('Dise{}PincodeAggregations'.format(session))
    if what == 'pincode':
        return pincode_model

    return [school_model, cluster_model, block_model, district_model, pincode_model]
