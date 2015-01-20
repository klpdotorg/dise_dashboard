from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404, redirect
from collections import OrderedDict

from .serializers import (
    SchoolSerializer, ClusterSerializer, BlockSerializer,
    DistrictSerializer, AssemblySerializer, ParliamentSerializer,
    PincodeSerializer
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
    bbox_filter_field = SchoolSerializer.Meta.geometry_field
    filter_backends = (filters.KLPInBBOXFilter, filters.TextSearchFilter, )

    def get_bbox_filter_field(self):
        return self.bbox_filter_field

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


class AggregationBaseView(object):
    filter_backends = (filters.KLPInBBOXFilter, filters.TextSearchFilter, )

    def get_bbox_filter_field(self):
        filter_field = ''
        if hasattr(self, 'bbox_filter_field'):
            filter_field = self.bbox_filter_field
        else:
            serializer = self.get_serializer_class()
            try:
                filter_field = serializer.Meta.geometry_field
            except:
                raise APIException(
                    'No bbox_filter_field provided in the view or '
                    'geometry_field provided in the serializer'
                )
        return filter_field

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
        session = self.kwargs.get('session')
        entity = self.kwargs.get('entity')
        entity_name = self.kwargs.get('entity_name')
        serializer = serializers.get(entity)

        filters = {}
        filters['{}__iexact'.format(serializer.Meta.pk_field)] = entity_name

        try:
            obj = get_object_or_404(queryset, **filters)
        except Exception as e:
            raise APIException(e)
        return obj


class AggregationSchoolListView(SchoolApiBaseView, generics.ListAPIView):
    def get_queryset(self):
        queryset = super(AggregationSchoolListView, self).get_queryset()
        entity_name = self.kwargs.get('entity_name', None)
        entity = self.kwargs.get('entity')
        serializer = serializers.get(entity)

        queryset = queryset.filter(**{
            '{}__iexact'.format(serializer.Meta.pk_field): entity_name
        })
        return queryset


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
        )

    return Response(endpoints)
