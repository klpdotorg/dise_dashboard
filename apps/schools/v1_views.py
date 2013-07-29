from django.views.generic import View, FormView, TemplateView
from django.db.models import Count, Min, Sum, Avg
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json
from django.core import serializers

from common.views import JSONResponseMixin
from schools.models import YearlyData, School


class V1SearchView(View, JSONResponseMixin):
    def get(self, *args, **kwargs):
        params = self.request.GET
        query = {}

        if params.get('area_type', ''):
            query['yearlydata__area_type'] = params.get('area_type', '')

        if params.get('building_status', ''):
            query['yearlydata__building_status'] = params.get('building_status', '')

        limit = int(params.get('limit', 20))
        schools = School.objects.order_by('id')

        if params.get('no_toilet', 'off') == 'on':
            schools = schools.annotate(total_toilets=Sum('yearlydata__toilet__count'))
            query['total_toilets'] = 0

        schools = schools.filter(**query)[:limit]
        schools_json = serializers.serialize("json", schools)
        return self.get_json_response(schools_json)
