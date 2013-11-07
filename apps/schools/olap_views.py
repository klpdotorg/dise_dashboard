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
from schools.olap_models import Dise1011BasicData, School, Cluster

# This shall become 0 when we have the map
DEFAULT_LIMIT = 20


class OLAPEndPoint(View, JSONResponseMixin):
    def get(self, *args, **kwargs):
        params = self.request.GET
        results = {}
        json_results = ''

        try:
            method = params['method']
            entity_name, endpoint_name = method.split('.')
            entity = globals().get(entity_name)
            endpoint = getattr(entity, endpoint_name)
            json_results = endpoint(params)
        except (KeyError, ValueError, ImportError, AttributeError) as e:
            results['error'] = str(e)
            json_results = json.dumps(results)
            return self.get_json_response(json_results)

        return self.get_json_response(json_results)