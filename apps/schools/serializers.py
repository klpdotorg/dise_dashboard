from .olap_models import (
    BasicData, ClusterAggregations, BlockAggregations,
    DistrictAggregations, AssemblyAggregations, ParliamentAggregations,
    PincodeAggregations
)
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
            'toilet_girls', 'tot_clrooms', 'popup_content', 'entity_type'
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


class AggregationBaseSerializer(GeoFeatureModelSerializer):
    medium_of_instructions = serializers.SerializerMethodField()

    def get_medium_of_instructions(self, obj):
        return obj.medium_of_instructions


class ClusterSerializer(AggregationBaseSerializer):
    class Meta:
        model = ClusterAggregations
        geo_field = 'centroid'
        pk_field = 'cluster_name'
        fields = ClusterAggregations._meta.get_all_field_names() + ['entity_type', 'popup_content']


class BlockSerializer(AggregationBaseSerializer):
    class Meta:
        model = BlockAggregations
        geo_field = 'centroid'
        pk_field = 'block_name'
        fields = BlockAggregations._meta.get_all_field_names() + ['entity_type', 'popup_content']


class DistrictSerializer(AggregationBaseSerializer):
    class Meta:
        model = DistrictAggregations
        geo_field = 'centroid'
        pk_field = 'district'
        fields = DistrictAggregations._meta.get_all_field_names() + ['entity_type', 'popup_content']


class AssemblySerializer(AggregationBaseSerializer):
    class Meta:
        model = AssemblyAggregations
        geo_field = 'centroid'
        pk_field = 'assembly_name'
        fields = AssemblyAggregations._meta.get_all_field_names() + ['entity_type', 'popup_content']


class ParliamentSerializer(AggregationBaseSerializer):
    class Meta:
        model = ParliamentAggregations
        geo_field = 'centroid'
        pk_field = 'parliament_name'
        fields = ParliamentAggregations._meta.get_all_field_names() + ['entity_type', 'popup_content']


class PincodeSerializer(AggregationBaseSerializer):
    class Meta:
        model = PincodeAggregations
        geo_field = 'centroid'
        pk_field = 'pincode'
        fields = PincodeAggregations._meta.get_all_field_names() + ['entity_type', 'popup_content']
