from django.views.generic import View, FormView, TemplateView
from django.db.models import Count, Min, Sum, Avg, F, Q
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json
from django.core import serializers
from django.db import connection

from geojson import Feature, Point, dumps as geojson_dumps
import re

from common import SumCase
from common.views import JSONResponseMixin

from schools import olap_entities
# This shall become 0 when we have the map
DEFAULT_LIMIT = 20


class OLAPUnifiedSearch(View, JSONResponseMixin):
    def get(self, *args, **kwargs):
        school_api = School()
        params = self.request.GET
        results = []
        json_results = ''

        try:
            query = params.get('q')
            session = params.get('filters[session]')
            if session not in ['10-11', '11-12', '12-13']:
                raise ValueError('Session not valid')

            SchoolModel, ClusterModel, BlockModel, DistrictModel, PincodeModel = get_models(session, "all")

            schools = SchoolModel.objects.filter(school_name__icontains=query).order_by('school_name')[:3]

            if schools.count() > 0:
                temp_d = {
                    'text': 'Schools',
                    'children': []
                }
                for school in schools:
                    feature = {}
                    if school.centroid is not None:
                        feature = school_api._get_geojson(school)

                    temp_d['children'].append({
                        'type': 'school',
                        'id': school.school_code,
                        'text': school.school_name,
                        # 'centroid': [school.centroid.y, school.centroid.x] if school.centroid is not None else []
                        'feature': geojson_dumps(feature)
                    })
                results.append(temp_d)

            clusters = ClusterModel.objects.filter(cluster_name__icontains=query).order_by('cluster_name')[:3]
            if clusters.count() > 0:
                temp_d = {
                    'text': 'Clusters',
                    'children': []
                }
                for cluster in clusters:
                    temp_d['children'].append({
                        'type': 'cluster',
                        'id': cluster.cluster_name,
                        'text': cluster.cluster_name,
                    })
                results.append(temp_d)

            blocks = BlockModel.objects.filter(block_name__icontains=query).order_by('block_name')[:3]
            if blocks.count() > 0:
                temp_d = {
                    'text': 'Blocks',
                    'children': []
                }
                for block in blocks:
                    temp_d['children'].append({
                        'type': 'block',
                        'id': block.block_name,
                        'text': block.block_name,
                    })
                results.append(temp_d)

            districts = DistrictModel.objects.filter(district__icontains=query).order_by('district')[:3]
            if districts.count() > 0:
                temp_d = {
                    'text': 'Districts',
                    'children': []
                }
                for district in districts:
                    temp_d['children'].append({
                        'type': 'district',
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
            entities = {
                'School': olap_entities.School,
                'Cluster': olap_entities.Cluster,
                'Block': olap_entities.Block,
                'District': olap_entities.District,
                'Pincode': olap_entities.Pincode,
            }
            entity = entities.get(entity_name)

            # get the actual classmethod that returns JSON string
            endpoint = getattr(entity, endpoint_name)

            json_results = endpoint(params)
        except (KeyError, ValueError, ImportError, AttributeError) as e:
            results['error'] = str(e)
            json_results = json.dumps(results)
            return self.get_json_response(json_results)

        return self.get_json_response(json_results)
