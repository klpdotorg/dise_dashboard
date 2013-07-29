from django.views.generic import View, FormView, TemplateView
from django.db.models import Count, Min, Sum, Avg
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json
from django.core import serializers

from common import SumCase
from common.views import JSONResponseMixin
from schools.models import YearlyData, School


class V1SearchView(View, JSONResponseMixin):
    def get(self, *args, **kwargs):
        params = self.request.GET
        query = {}
        schools = School.objects.order_by('id').values('id', 'code', 'name')
        limit = int(params.get('limit', 20))

        if params.get('area_type', ''):
            schools = schools.filter(yearlydata__area_type=params.get('area_type', ''))

        if params.get('building_status', ''):
            schools = schools.filter(yearlydata__building_status=params.get('building_status', ''))

        if params.get('no_toilet', 'off') == 'on':
            schools = schools.annotate(total_toilets=Sum('yearlydata__toilet__count'))
            schools = schools.filter(total_toilets=0)

        if params.get('needs_repair', 'off') == 'on':
            schools = schools.annotate(
                repair_count=SumCase(
                    'yearlydata__room__count',
                    when='"schools_room"."type" = \'class\' AND "schools_room"."condition" IN (\'minor\', \'major\')'
                )
            )
            schools = schools.filter(repair_count__gt=0)

        schools = schools[:limit]
        print schools.query
        # schools_json = serializers.serialize("json", schools)
        return self.render_to_response(list(schools))
