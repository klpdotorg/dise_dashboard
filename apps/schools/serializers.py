from .models import (
    BasicData, ClusterAggregations, BlockAggregations,
    DistrictAggregations, AssemblyAggregations, ParliamentAggregations,
    PincodeAggregations
)
from common.models import MEDIUM, SCHOOL_CATEGORY, search_choices_by_key
from common import SumCase, CountWhen
from django.db.models import Count, Sum, Case, When
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class SchoolSerializer(GeoFeatureModelSerializer):
    library_yn = serializers.CharField(source='get_library_yn_display')
    drinking_water = serializers.CharField(source='get_drinking_water_display')
    electricity = serializers.CharField(source='get_electricity_display')
    medium_of_instruction = serializers.CharField(source='get_medium_of_instruction_display')
    sch_management = serializers.CharField(source='get_sch_management_display')
    sch_category = serializers.CharField(source='get_sch_category_display')
    entity_type = serializers.SerializerMethodField()

    def get_entity_type(self, obj):
        return 'school'

    class Meta:
        model = BasicData
        geo_field = 'centroid'
        pk_field = 'school_code'

        fields = [
            'school_code', 'school_name', 'cluster_name', 'centroid',
            'block_name', 'district', 'pincode', 'yeur_estd',
            'total_boys', 'total_girls', 'male_tch', 'female_tch',
            'medium_of_instruction', 'sch_management', 'sch_category',
            'library_yn', 'books_in_library', 'no_of_computers',
            'electricity', 'drinking_water', 'toilet_common', 'toilet_boys',
            'toilet_girls', 'tot_clrooms', 'school_dev_grant_recd', 
            'school_dev_grant_expnd', 'funds_from_students_recd',
            'funds_from_students_expnd', 'school_maintain_grant_recd',
            'school_maintain_grant_expnd', 'popup_content', 'entity_type'
        ]


class SchoolInfraSerializer(GeoFeatureModelSerializer):
    status_of_mdm = serializers.CharField(source='get_status_of_mdm_display')
    boundary_wall = serializers.CharField(source='get_boundary_wall_display')
    library_yn = serializers.CharField(source='get_library_yn_display')
    building_status = serializers.CharField(source='get_building_status_display')
    ramps = serializers.CharField(source='get_ramps_display')
    playground = serializers.CharField(source='get_playground_display')
    separate_room_for_headmaster = serializers.CharField(source='get_separate_room_for_headmaster_display')
    electricity = serializers.CharField(source='get_electricity_display')
    computer_aided_learnin_lab = serializers.CharField(source='get_computer_aided_learnin_lab_display')
    drinking_water = serializers.CharField(source='get_drinking_water_display')
    medical_checkup = serializers.CharField(source='get_medical_checkup_display')

    class Meta:
        model = BasicData
        geo_field = 'centroid'
        pk_field = 'school_code'

        fields = [
            'school_code', 'school_name', 'centroid',
            'status_of_mdm', 'drinking_water', 'building_status',
            'ramps', 'playground', 'boundary_wall', 'medical_checkup',
            'separate_room_for_headmaster', 'classrooms_require_major_repair',
            'classrooms_require_minor_repair', 'electricity', 'blackboard',
            'library_yn', 'books_in_library', 'computer_aided_learnin_lab',
            'no_of_computers', 'toilet_common', 'toilet_boys',
            'toilet_girls', 'tot_clrooms', 'popup_content'
        ]


class SchoolFinSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = BasicData
        geo_field = 'centroid'
        pk_field = 'school_code'

        fields = [
            'school_code', 'school_name', 'cluster_name', 'centroid',
            'block_name', 'district', 'pincode', 'yeur_estd',
            'school_dev_grant_recd', 
            'school_dev_grant_expnd', 'funds_from_students_recd',
            'funds_from_students_expnd', 'school_maintain_grant_recd',
            'school_maintain_grant_expnd', 'popup_content'
        ]


class AggregationBaseSerializer(GeoFeatureModelSerializer):
    medium_of_instructions = serializers.SerializerMethodField()
    school_categories = serializers.SerializerMethodField()

    def get_medium_of_instructions(self, obj):
        moes = obj.schools(obj.session).values('medium_of_instruction').annotate(
            sum_schools=Count('medium_of_instruction'),
            sum_boys=Sum('total_boys'),
            sum_girls=Sum('total_girls')
        )
        for moe in moes:
            moe['id'] = moe['medium_of_instruction']
            moe['name'] = search_choices_by_key(MEDIUM, moe['id'])
            del moe['medium_of_instruction']

        moes = sorted(moes, key=lambda k: k['sum_schools'], reverse=True)
        return moes

    def get_school_categories(self, obj):
        print("Object session: ", obj.session)
        print("Object schools:", obj.schools)
        categories = obj.schools(obj.session).values('sch_category').annotate(
            sum_schools_total=Count('sch_category'),
            sum_schools_classrooms_leq_3=Count(Case(When(tot_clrooms__lte=3, then=1))),
            sum_schools_classrooms_eq_4=Count(Case(When(tot_clrooms=4, then=1))),
            sum_schools_classrooms_eq_5=Count(Case(When(tot_clrooms=5, then=1))),
            sum_schools_classrooms_mid_67=Count(Case(When(tot_clrooms__in=[6,7], then=1))),
            sum_schools_classrooms_geq_8=Count(Case(When(tot_clrooms__gte=8, then=1))),
            sum_boys=Sum('total_boys'),
            sum_girls=Sum('total_girls'),
            sum_classrooms=Sum('tot_clrooms'),
        )
        print(categories)
        for category in categories:
            category['id'] = category['sch_category']
            category['name'] = search_choices_by_key(SCHOOL_CATEGORY, category['id'])
            del category['sch_category']

            category_copy = category.copy()
            category['sum_schools'] = dict()
            for key, value in category_copy.items():
                if key.startswith('sum_schools'):
                    category['sum_schools'][key.replace('sum_schools_', '')] = value
                    del category[key]

        categories = sorted(categories, key=lambda k: k['id'])
        return categories


class ClusterSerializer(AggregationBaseSerializer):
    class Meta:
        model = ClusterAggregations
        geo_field = 'centroid'
        pk_field = 'cluster_name'
        fields = [field.name for field in ClusterAggregations._meta.get_fields()] + [
            'entity_type', 'popup_content', 'medium_of_instructions', 'school_categories'
        ]


class BlockSerializer(AggregationBaseSerializer):
    class Meta:
        model = BlockAggregations
        geo_field = 'centroid'
        pk_field = 'block_name'
        fields = [field.name for field in BlockAggregations._meta.get_fields()] + [
            'entity_type', 'popup_content', 'medium_of_instructions', 'school_categories'
        ]


class DistrictSerializer(AggregationBaseSerializer):
    class Meta:
        model = DistrictAggregations
        geo_field = 'centroid'
        id_field = 'district'
        fields = [field.name for field in DistrictAggregations._meta.get_fields()] + [
            'entity_type', 'popup_content', 'medium_of_instructions', 'school_categories'
        ]


class ClusterBasicSerializer(AggregationBaseSerializer):
    # Returns just names, no aggregated values
    class Meta:
        model = ClusterAggregations
        geo_field = 'centroid'
        pk_field = 'cluster_name'
        fields = ['cluster_name', 'slug', 'block_name', 'district', 'centroid']


class BlockBasicSerializer(AggregationBaseSerializer):
    # Returns just names, no aggregated values
    class Meta:
        model = BlockAggregations
        geo_field = 'centroid'
        pk_field = 'block_name'
        fields = ['block_name', 'slug', 'district', 'centroid']


class DistrictBasicSerializer(AggregationBaseSerializer):
    # Returns just names, no aggregated values
    class Meta:
        model = DistrictAggregations
        geo_field = 'centroid'
        pk_field = 'district'
        fields = ['district', 'slug', 'centroid']


class AssemblySerializer(AggregationBaseSerializer):
    class Meta:
        model = AssemblyAggregations
        geo_field = 'centroid'
        pk_field = 'assembly_name'
        fields = [field.name for field in AssemblyAggregations._meta.get_fields()] + [
            'entity_type', 'popup_content', 'medium_of_instructions', 'school_categories'
        ]


class ParliamentSerializer(AggregationBaseSerializer):
    class Meta:
        model = ParliamentAggregations
        geo_field = 'centroid'
        pk_field = 'parliament_name'
        fields = [field.name for field in ParliamentAggregations._meta.get_fields()] + [
            'entity_type', 'popup_content', 'medium_of_instructions', 'school_categories'
        ]


class PincodeSerializer(AggregationBaseSerializer):
    class Meta:
        model = PincodeAggregations
        geo_field = 'centroid'
        pk_field = 'pincode'
        fields = [field.name for field in PincodeAggregations._meta.get_fields()] + [
            'entity_type', 'popup_content', 'medium_of_instructions', 'school_categories'
        ]

def get_models(session='10-11', what='all'):
    session = session.replace('-', '')
    schools = __import__('schools')
    models = collections.OrderedDict()

    models['school'] = getattr(
        schools.models, 'Dise{}BasicData'.format(session)
    )
    models['cluster'] = getattr(
        schools.models, 'Dise{}ClusterAggregations'.format(session)
    )
    models['block'] = getattr(
        schools.models, 'Dise{}BlockAggregations'.format(session)
    )
    models['district'] = getattr(
        schools.models, 'Dise{}DistrictAggregations'.format(session)
    )
    models['pincode'] = getattr(
        schools.models, 'Dise{}PincodeAggregations'.format(session)
    )
    models['assembly'] = getattr(
        schools.models, 'Dise{}AssemblyAggregations'.format(session)
    )
    models['parliament'] = getattr(
        schools.models, 'Dise{}ParliamentAggregations'.format(session)
    )

    if what == 'all':
        return models.values()
    else:
        return models.get(what, None)