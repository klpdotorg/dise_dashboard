from django.views.generic import View, FormView, TemplateView
from django.db.models import Count, Min, Sum, Avg, F, Q
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json
from django.core import serializers
from django.db import connection

import geojson
import re

from common import SumCase
from common.views import JSONResponseMixin
from schools.models import YearlyData, School, SchoolManaagement,\
    DrinkingWaterSource, BoundaryWallType, search_choices, YESNO, MDM_STATUS
from schools.olap_models import Dise1011AssemblyAggregations, \
    Dise1112AssemblyAggregations, Dise1213AssemblyAggregations, \
    Dise1011BlockAggregations, Dise1112BlockAggregations, \
    Dise1213BlockAggregations, Dise1011ClusterAggregations, \
    Dise1112ClusterAggregations, Dise1213ClusterAggregations, \
    Dise1011ParliamentAggregations, Dise1112ParliamentAggregations, \
    Dise1213ParliamentAggregations, Dise1011DistrictAggregations, \
    Dise1112DistrictAggregations, Dise1213DistrictAggregations, \
    Dise1011BasicData, Dise1112BasicData, Dise1213BasicData, School, Cluster

# This shall become 0 when we have the map
DEFAULT_LIMIT = 20

def get_models(session='10-11'):
    school_model = globals().get('Dise{}BasicData'.format(session.replace('-', '')))
    cluster_model = globals().get('Dise{}ClusterAggregations'.format(session.replace('-', '')))
    block_model = globals().get('Dise{}BlockAggregations'.format(session.replace('-', '')))
    district_model = globals().get('Dise{}DistrictAggregations'.format(session.replace('-', '')))
    return school_model, cluster_model, block_model, district_model


class OLAPUnifiedSearch(View, JSONResponseMixin):
    def get(self, *args, **kwargs):
        params = self.request.GET
        results = []
        json_results = ''

        try:
            query = params.get('q')
            session = params.get('filters[session]')
            if session not in ['10-11', '11-12', '12-13']:
                raise ValueError('Session not valid')

            School, Cluster, Block, District = get_models(session)

            schools = School.objects.filter(school_name__icontains=query).order_by('school_name')[:3]
            if schools.count() > 0:
                temp_d = {
                    'text': 'Schools',
                    'children': []
                }
                for school in schools:
                    temp_d['children'].append({
                        'id': school.school_code,
                        'text': school.school_name,
                        'centroid': [school.centroid.y, school.centroid.x] if school.centroid is not None else []
                    })
                results.append(temp_d)

            clusters = Cluster.objects.filter(cluster_name__icontains=query).order_by('cluster_name')[:3]
            if clusters.count() > 0:
                temp_d = {
                    'text': 'Clusters',
                    'children': []
                }
                for cluster in clusters:
                    temp_d['children'].append({
                        'id': cluster.cluster_name,
                        'text': cluster.cluster_name,
                    })
                results.append(temp_d)

            blocks = Block.objects.filter(block_name__icontains=query).order_by('block_name')[:3]
            if blocks.count() > 0:
                temp_d = {
                    'text': 'Blocks',
                    'children': []
                }
                for block in blocks:
                    temp_d['children'].append({
                        'id': block.block_name,
                        'text': block.block_name,
                    })
                results.append(temp_d)

            districts = District.objects.filter(district__icontains=query).order_by('district')[:3]
            if districts.count() > 0:
                temp_d = {
                    'text': 'Districts',
                    'children': []
                }
                for district in districts:
                    temp_d['children'].append({
                        'id': district.district,
                        'text': district.district,
                    })
                results.append(temp_d)

            json_results = json.dumps(results)
        except (KeyError, ValueError, ImportError, AttributeError) as e:
            # results['error'] = str(e)
            print str(e)
            results = []
            json_results = json.dumps(results)
            return self.get_json_response(json_results)

        return self.get_json_response(json_results)

class OLAPEndPoint(View, JSONResponseMixin):
    def get(self, *args, **kwargs):
        params = self.request.GET
        results = {}
        json_results = ''

        try:
            # method would be like `School.getInfo`
            method = params['method']

            # School, getInfo
            entity_name, endpoint_name = method.split('.')

            # Make sure School, Cluster and other entities are imported
            # for this to work
            entity = globals().get(entity_name)

            # get the actual classmethod that returns JSON string
            endpoint = getattr(entity, endpoint_name)

            json_results = endpoint(params)
        except (KeyError, ValueError, ImportError, AttributeError) as e:
            results['error'] = str(e)
            json_results = json.dumps(results)
            return self.get_json_response(json_results)

        return self.get_json_response(json_results)