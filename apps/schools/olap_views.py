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
from schools.olap_models import Dise1011BasicData, Dise1112BasicData, School, Cluster

# This shall become 0 when we have the map
DEFAULT_LIMIT = 20


class OLAPUnifiedSearch(View, JSONResponseMixin):
    def get(self, *args, **kwargs):
        params = self.request.GET
        results = {}
        json_results = ''

        try:
            results = {
                "schools": [
                    {
                        "cluster_name": "CH DAPKA",
                        "block_name": "AURAD",
                        "school_code": 29050115601,
                        "school_name": "GOVT MPS CH.DABKA"
                    },
                    {
                        "cluster_name": "BHANTANUR",
                        "block_name": "MUDHOL",
                        "school_code": 29021110601,
                        "school_name": "GOVT LPS PALKIMA NYA ARALIKATTI"
                    },
                    {
                        "cluster_name": "BHANTANUR",
                        "block_name": "MUDHOL",
                        "school_code": 29021101802,
                        "school_name": "GOVT LPS CHIKKUR LT"
                    },
                    {
                        "cluster_name": "BHANTANUR",
                        "block_name": "MUDHOL",
                        "school_code": 29021100702,
                        "school_name": "GOVT LPS BANTANUR JANATA PLOT"
                    },
                    {
                        "cluster_name": "SURGAON",
                        "block_name": "MUDHOL",
                        "school_code": 29021104108,
                        "school_name": "GOVT LPS HUNSIGADDI TOTA KULALI"
                    }
                ],
                "clusters": [
                    {
                        "cluster_name": "BARAGAON",
                        "block_name": "KHANAPUR",
                        "district": "BELGAUM",
                        "village_name": "NIDGAL"
                    },
                    {
                        "cluster_name": "BORGAON",
                        "block_name": "NIPPANI",
                        "district": "CHIKKODI",
                        "village_name": "BORGAON"
                    },
                    {
                        "cluster_name": "CHAPGAON",
                        "block_name": "KHANAPUR",
                        "district": "BELGAUM",
                        "village_name": "KODACHAWAD"
                    },
                    {
                        "cluster_name": "DEVANAGAON",
                        "block_name": "SINDAGI",
                        "district": "BIJAPUR",
                        "village_name": "KADLEWAD (PA)"
                    },
                    {
                        "cluster_name": "DONGAON (M)",
                        "block_name": "AURAD",
                        "district": "BIDAR",
                        "village_name": "KOTAGYAL"
                    },
                ]
            }
            json_results = json.dumps(results)
        except (KeyError, ValueError, ImportError, AttributeError) as e:
            results['error'] = str(e)
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