from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from collections import OrderedDict

from .serializers import (
    SchoolSerializer, ClusterSerializer, BlockSerializer,
    DistrictSerializer, AssemblySerializer, ParliamentSerializer,
    PincodeSerializer, SchoolInfraSerializer
)
serializers = {
    'cluster': ClusterSerializer,
    'block': BlockSerializer,
    'district': DistrictSerializer,
    'assembly': AssemblySerializer,
    'parliament': ParliamentSerializer,
    'pincode': PincodeSerializer,
}
from .olap_models import get_models
from common import filters


class SessionNotFound(APIException):
    status_code = 404
    default_detail = 'Session not found. Please enter a valid session.'


class EntityNotFound(APIException):
    status_code = 404
    default_detail = 'Entity not found. Please enter a valid entity.'


class SchoolApiBaseView(object):
    serializer_class = SchoolSerializer
    bbox_filter_field = SchoolSerializer.Meta.geo_field
    filter_backends = (filters.KLPInBBOXFilter, filters.TextSearchFilter, )

    def get_queryset(self):
        session = self.kwargs.get('session')

        try:
            SchoolData = get_models(session, 'school')
        except AttributeError:
            raise SessionNotFound()

        return SchoolData.objects.all()


class SchoolListView(SchoolApiBaseView, generics.ListAPIView):
    """Returns the list of schools for given year and filters
    """
    pass


class SchoolInfoView(SchoolApiBaseView, generics.RetrieveAPIView):
    """Returns details of the given school
    """
    def get_object(self):
        queryset = self.get_queryset()
        filters = {}
        filters['school_code__iexact'] = self.kwargs.get('dise_code')
        obj = get_object_or_404(queryset, **filters)
        return obj


class SchoolInfraView(SchoolInfoView):
    serializer_class = SchoolInfraSerializer


class AggregationBaseView(object):
    filter_backends = (filters.KLPInBBOXFilter, filters.TextSearchFilter, )
    bbox_filter_field = 'centroid'

    def get_serializer_class(self):
        entity = self.kwargs.get('entity')
        serializer = serializers.get(entity)
        return serializer

    def get_queryset(self):
        session = self.kwargs.get('session')
        entity = self.kwargs.get('entity')

        try:
            Entity = get_models(session, entity)
        except AttributeError:
            raise SessionNotFound()

        return Entity.objects.all()


class AggregationListView(AggregationBaseView, generics.ListAPIView):
    pass


class AggregationInfoView(AggregationBaseView, generics.RetrieveAPIView):
    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get('slug')

        filters = {
            'slug__iexact': slug
        }

        try:
            obj = get_object_or_404(queryset, **filters)
        except Exception as e:
            raise APIException(e)
        return obj


class AggregationSchoolListView(SchoolApiBaseView, generics.ListAPIView):
    """Lists all the schools in the given aggregated entity_obj
    """
    def get_queryset(self):
        # get all schools
        schools = super(AggregationSchoolListView, self).get_queryset()

        slug = self.kwargs.get('slug', None)
        entity = self.kwargs.get('entity')
        serializer = serializers.get(entity)
        session = self.kwargs.get('session')
        entity = self.kwargs.get('entity')

        # get the entity model
        try:
            EntityModel = get_models(session, entity)
        except AttributeError:
            raise SessionNotFound()

        # get the entity object
        entity_obj = EntityModel.objects.get(slug=slug)

        # if entity has district, filter schools in same district
        if hasattr(entity_obj, 'district'):
            schools = schools.filter(district__iexact=entity_obj.district)

        filters = {
            '{}__iexact'.format(serializer.Meta.pk_field): str(
                getattr(entity_obj, serializer.Meta.pk_field)
            ),
        }

        # if entity is pincode, search both pincode OR new_pincode field
        if entity == 'pincode':
            filters['new_pincode__iexact'] = str(
                getattr(entity_obj, serializer.Meta.pk_field)
            )

            q_list = [Q(f) for f in filters.items()]

            import operator
            return schools.filter(reduce(operator.or_, q_list))

        return schools.filter(**filters)


class ClustersInBlockView(AggregationListView, generics.ListAPIView):
    """Lists all the clusters in a block"""
    def get_queryset(self):
        session = self.kwargs.get('session')
        block_slug = self.kwargs.get('block_slug')

        # We need to query the cluster_aggregations model
        try:
            ClusterModel = get_models(session, 'cluster')
            BlockModel = get_models(session, 'block')
        except AttributeError:
            raise SessionNotFound()

        block = get_object_or_404(BlockModel, slug=block_slug)
        clusters = ClusterModel.objects.filter(
            block_name__iexact=block.block_name
        )
        return clusters


class ClustersInDistrictView(AggregationListView, generics.ListAPIView):
    """Lists all the clusters in a district"""
    def get_queryset(self):
        session = self.kwargs.get('session')
        district_slug = self.kwargs.get('district_slug')

        # We need to query the cluster_aggregations model
        try:
            ClusterModel = get_models(session, 'cluster')
            DistrictModel = get_models(session, 'district')
        except AttributeError:
            raise SessionNotFound()

        district = get_object_or_404(DistrictModel, slug=district_slug)
        clusters = ClusterModel.objects.filter(
            district__iexact=district.district
        )
        return clusters


class BlocksInDistrictView(AggregationListView, generics.ListAPIView):
    """Lists all the blocks in a district"""
    def get_queryset(self):
        session = self.kwargs.get('session')
        district_slug = self.kwargs.get('district_slug')

        # We need to query the block_aggregations model
        try:
            BlockModel = get_models(session, 'block')
            DistrictModel = get_models(session, 'district')
        except AttributeError:
            raise SessionNotFound()

        district = get_object_or_404(DistrictModel, slug=district_slug)
        blocks = BlockModel.objects.filter(district__iexact=district.district)
        return blocks


@api_view(('GET',))
def api_root(request, format=None):
    endpoints = OrderedDict()
    endpoints['School List'] = reverse(
        'api_school_list', request=request, args=['12-13']
    )
    endpoints['School Info'] = reverse(
        'api_school_info', request=request, args=['12-13', '29310306103']
    )

    for entity in serializers.keys():
        endpoints['%s List' % entity.title()] = reverse(
            'api_entity_list', request=request, args=['12-13', entity]
        ) + "?bbox=76.10589981079102,15.00581078905935,76.34038925170898,15.074775626862015"

    endpoints['Cluster Info'] = reverse(
        'api_entity_info', request=request,
        args=['12-13', 'cluster', 'davanageren-avaragere']
    )
    endpoints['Schools in Cluster'] = reverse(
        'api_entity_school_list', request=request,
        args=['12-13', 'cluster', 'davanageren-avaragere']
    )
    endpoints['Block Info'] = reverse(
        'api_entity_info', request=request,
        args=['12-13', 'block', 'gulbarga-afzalpur']
    )
    endpoints['Schools in Block'] = reverse(
        'api_entity_school_list', request=request,
        args=['12-13', 'block', 'gulbarga-afzalpur']
    )
    endpoints['Clusters in Block'] = reverse(
        'api_clusters_in_block', request=request,
        args=['12-13', 'block', 'gulbarga-afzalpur']
    )
    endpoints['District Info'] = reverse(
        'api_entity_info', request=request,
        args=['12-13', 'district', 'bagalkot']
    )
    endpoints['Schools in District'] = reverse(
        'api_entity_school_list', request=request,
        args=['12-13', 'district', 'bagalkot']
    )
    endpoints['Clusters in District'] = reverse(
        'api_clusters_in_district', request=request,
        args=['12-13', 'district', 'bagalkot']
    )
    endpoints['Blocks in District'] = reverse(
        'api_blocks_in_district', request=request,
        args=['12-13', 'district', 'bagalkot']
    )
    endpoints['Assembly Info'] = reverse(
        'api_entity_info', request=request,
        args=['12-13', 'assembly', 'bhadravati']
    )
    endpoints['Schools in Assembly'] = reverse(
        'api_entity_school_list', request=request,
        args=['12-13', 'assembly', 'bhadravati']
    )
    endpoints['Parliament Info'] = reverse(
        'api_entity_info', request=request,
        args=['12-13', 'parliament', 'bagalkot']
    )
    endpoints['Schools in Parliament'] = reverse(
        'api_entity_school_list', request=request,
        args=['12-13', 'parliament', 'bagalkot']
    )
    endpoints['Pincode Info'] = reverse(
        'api_entity_info', request=request,
        args=['12-13', 'pincode', '560044']
    )
    endpoints['Schools in Pincode'] = reverse(
        'api_entity_school_list', request=request,
        args=['12-13', 'pincode', '560044']
    )

    return Response(endpoints)
