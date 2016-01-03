from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.conf import settings
from collections import OrderedDict
import operator

from .serializers import (
    SchoolSerializer, ClusterSerializer, BlockSerializer,
    DistrictSerializer, AssemblySerializer, ParliamentSerializer,
    PincodeSerializer, SchoolInfraSerializer,
    ClusterBasicSerializer, BlockBasicSerializer, DistrictBasicSerializer
)

from .models import get_models
from common import filters
from common import models as common_utils

serializers = {
    'cluster': ClusterSerializer,
    'cluster-basic': ClusterBasicSerializer,
    'block': BlockSerializer,
    'block-basic': BlockBasicSerializer,
    'district': DistrictSerializer,
    'district-basic': DistrictBasicSerializer,
    'assembly': AssemblySerializer,
    'parliament': ParliamentSerializer,
    'pincode': PincodeSerializer,
}


class SessionNotFound(APIException):
    status_code = 404
    default_detail = 'Session not found. Please enter a valid session.'


class EntityNotFound(APIException):
    status_code = 404
    default_detail = 'Entity not found. Please enter a valid entity.'


class NotFound(APIException):
    status_code = 404


class OmniSearchApiView(APIView):
    def get(self, request, session=settings.DEFAULT_SESSION, format=None):
        """Searches all entities together or individually
        ---
        parameters:
            - name: session
              required: true
              description: the session to search for, in the format "14-15". Default is latest session.
            - name: query
              required: true
              description: the term to search for
            - name: type
              description: "entity type to search for. options are - school,
                            cluster, block, district, pincode, assembly,
                            parliament and all. Default is 'all'."
        """

        session = self.kwargs.get('session', session)
        query = request.query_params.get('query')
        if not query:
            raise NotFound('URL parameter "query" does not exist.')

        query_variations = [
            query,
            query.replace('-', ''),
            query.replace('-', ' '),
            query.replace('.', '')
        ]

        stype = request.query_params.get('type', 'all')

        results = []

        try:
            SchoolModel = get_models(session, 'school')
            ClusterModel = get_models(session, 'cluster')
            BlockModel = get_models(session, 'block')
            DistrictModel = get_models(session, 'district')
            PincodeModel = get_models(session, 'pincode')
            AssemblyModel = get_models(session, 'assembly')
            ParliamentModel = get_models(session, 'parliament')
        except AttributeError:
            raise SessionNotFound()

        if stype in ('school', 'all'):
            # search schools
            schools = SchoolModel.objects.filter(
                Q(school_name__icontains=query) | Q(school_code__icontains=query)
            ).order_by('school_name')[:3]

            if schools.count() > 0:
                temp_d = {
                    'text': 'Schools',
                    'children': []
                }
                for school in schools:
                    feature = SchoolSerializer(school)
                    temp_d['children'].append({
                        'type': 'school',
                        'id': school.school_code,
                        'text': school.school_name,
                        # 'centroid': [school.centroid.y, school.centroid.x] if school.centroid is not None else []
                        'feature': feature.data
                    })

                results.append(temp_d)

        if stype in ('cluster', 'all'):
            # search clusters
            clusters = ClusterModel.objects.filter(
                reduce(operator.or_, (Q(cluster_name__icontains=query) for query in query_variations))
            ).order_by('cluster_name')[:3]
            if clusters.count() > 0:
                temp_d = {
                    'text': 'Clusters',
                    'children': []
                }
                for cluster in clusters:
                    temp_d['children'].append({
                        'type': 'cluster',
                        'id': cluster.slug,
                        'text': cluster.cluster_name,
                    })
                results.append(temp_d)

        if stype in ('block', 'all'):
            blocks = BlockModel.objects.filter(
                reduce(operator.or_, (Q(block_name__icontains=query) for query in query_variations))
            ).order_by('block_name')[:3]
            if blocks.count() > 0:
                temp_d = {
                    'text': 'Blocks',
                    'children': []
                }
                for block in blocks:
                    temp_d['children'].append({
                        'type': 'block',
                        'id': block.slug,
                        'text': block.block_name,
                    })
                results.append(temp_d)

        if stype in ('district', 'all'):
            districts = DistrictModel.objects.filter(district__icontains=query).order_by('district')[:3]
            if districts.count() > 0:
                temp_d = {
                    'text': 'Ed. Dept. Districts',
                    'children': []
                }
                for district in districts:
                    temp_d['children'].append({
                        'type': 'district',
                        'id': district.slug,
                        'text': district.district,
                    })
                results.append(temp_d)

        if stype in ('pincode', 'all'):
            pincodes = PincodeModel.objects.filter(pincode__icontains=query).order_by('pincode')[:3]
            if pincodes.count() > 0:
                temp_d = {
                    'text': 'Pincodes',
                    'children': []
                }
                for pincode in pincodes:
                    temp_d['children'].append({
                        'type': 'pincode',
                        'id': pincode.pincode,
                        'text': str(pincode.pincode),
                    })
                results.append(temp_d)

        if stype in ('assembly', 'all'):
            assemblies = AssemblyModel.objects.filter(assembly_name__icontains=query).order_by('assembly_name')[:3]
            if assemblies.count() > 0:
                temp_d = {
                    'text': 'Assembly Constituencies',
                    'children': []
                }
                for assembly in assemblies:
                    temp_d['children'].append({
                        'type': 'assembly',
                        'id': assembly.slug,
                        'text': str(assembly.assembly_name),
                    })
                results.append(temp_d)

        if stype in ('parliament', 'all'):
            parliaments = ParliamentModel.objects.filter(parliament_name__icontains=query).order_by('parliament_name')[:3]
            if parliaments.count() > 0:
                temp_d = {
                    'text': 'Parliamentary Constituencies',
                    'children': []
                }
                for parliament in parliaments:
                    temp_d['children'].append({
                        'type': 'parliament',
                        'id': parliament.slug,
                        'text': str(parliament.parliament_name),
                    })
                results.append(temp_d)

        return Response(results)


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
        ---
        parameters:
            - name: session
              required: true
              description: the session to search for, in the format "14-15". Default is latest session.
            - name: management
              description: 'govt' or 'pvt'
            - name: area
              description: 'rural' or 'urban'
        """
    def get_queryset(self):
        queryset = super(SchoolListView, self).get_queryset()

        if 'management' in self.request.query_params and self.request.query_params.get('management', ''):
            if self.request.query_params.get('management') == 'govt':
                queryset = queryset.filter(
                    sch_management__in=[1, 7]
                )
            elif self.request.query_params.get('management') == 'pvt':
                queryset = queryset.exclude(
                    sch_management__in=[1, 7]
                )

        if 'area' in self.request.query_params and self.request.query_params.get('area', ''):
            queryset = queryset.filter(
                rural_urban=common_utils.search_choices(
                    common_utils.AREA, self.request.query_params.get('area').title()
                )
            )

        return queryset


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
    """Returns infrastructure details of a given school
    """
    serializer_class = SchoolInfraSerializer


class AggregationBaseView(object):
    filter_backends = (filters.KLPInBBOXFilter, filters.TextSearchFilter, )
    bbox_filter_field = 'centroid'

    def get_serializer_class(self):
        try:
            serializer = super(AggregationBaseView, self).get_serializer_class()
        except Exception, e:
            entity = self.kwargs.get('entity')
            basic = self.request.GET.get('basic', 'no')

            if basic == 'yes':
                serializer = serializers.get(entity + '-basic')
            else:
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
    def get(self, *args, **kwargs):
        """Lists aggregated entities depending on entity type. options for 'entity'
            are school, cluster, block, district, pincode, assembly and parliament.
            ---
            parameters:
                - name: session
                  required: true
                  description: the session to search for, in the format "14-15". Default is latest session.
                  paramType: path
                - name: entity
                  required: true
                  description: school, cluster, block, district, pincode, assembly and parliament.
                  paramType: path
                - name: basic
                  required: false
                  description: whether to return only basic data. default is 'no'. options are 'yes' or 'no'.
                  paramType: query

        """
        """
        This get() is here so that Swagger parses the docstring properly
        """
        return super(AggregationListView, self).get(*args, **kwargs)


class AggregationInfoView(AggregationBaseView, generics.RetrieveAPIView):
    def get(self, *args, **kwargs):
        """Shows details of aggregated entities depending on entity type and slug. options for 'entity'
            are school, cluster, block, district, pincode, assembly and parliament.
            ---
            parameters:
                - name: session
                  required: true
                  description: the session to search for, in the format "14-15". Default is latest session.
                - name: entity
                  required: true
                  description: school, cluster, block, district, pincode, assembly and parliament.
                - name: slug
                  required: true
                  description: slug of the given entity
        """
        """
        This get() is here so that Swagger parses the docstring properly
        """
        return super(AggregationInfoView, self).get(*args, **kwargs)

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
            'centroid__isnull': False
        }

        return schools.filter(**filters)


class ClustersInBlockView(AggregationListView, generics.ListAPIView):
    """Lists all the clusters in a block"""
    serializer_class = ClusterBasicSerializer

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
            block_name__iexact=block.block_name,
            centroid__isnull=False
        )
        return clusters


class ClustersInDistrictView(AggregationListView, generics.ListAPIView):
    """Lists all the clusters in a district"""
    serializer_class = ClusterBasicSerializer

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
            district__iexact=district.district,
            centroid__isnull=False
        )
        return clusters


class BlocksInDistrictView(AggregationListView, generics.ListAPIView):
    """Lists all the blocks in a district"""
    serializer_class = BlockBasicSerializer

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
        blocks = BlockModel.objects.filter(
            district__iexact=district.district,
            centroid__isnull=False
        )
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
