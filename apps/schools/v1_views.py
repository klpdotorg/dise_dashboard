from django.views.generic import View, FormView, TemplateView
from django.db.models import Count, Min, Sum, Avg
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json
from django.core import serializers

from common import SumCase
from common.views import JSONResponseMixin
from schools.models import YearlyData, School, search_choices, YESNO


class V1SearchView(View, JSONResponseMixin):
    def get(self, *args, **kwargs):
        params = self.request.GET
        results = {}
        schools = School.objects.values('id', 'code', 'name')
        limit = int(params.get('limit', 20))

        if params.get('year', ''):
            schools = schools.filter(yearlydata__academic_year__id=params.get('year', ''))

        if params.get('area_type', ''):
            schools = schools.filter(yearlydata__area_type=params.get('area_type', ''))

        if params.get('building_status', ''):
            schools = schools.filter(yearlydata__building_status=params.get('building_status', ''))

        if params.get('no_electricity', ''):
            schools = schools.filter(yearlydata__electricity_status=search_choices(YESNO, 'No'))

        if params.get('no_library', ''):
            schools = schools.filter(yearlydata__library_available=search_choices(YESNO, 'No'))

        if params.get('no_ramp', ''):
            schools = schools.filter(yearlydata__ramp_available=search_choices(YESNO, 'No'))

        if params.get('no_playground', ''):
            schools = schools.filter(yearlydata__playground_available=search_choices(YESNO, 'No'))

        if params.get('no_medical', ''):
            schools = schools.filter(yearlydata__medical_checkup=search_choices(YESNO, 'No'))

        if params.get('no_water', ''):
            schools = schools.filter(yearlydata__drinking_water_source__name__iexact="None")

        if params.get('no_toilet', 'off') == 'on':
            schools = schools.annotate(total_toilets=Sum('yearlydata__toilet__count'))
            schools = schools.filter(total_toilets=0)

        if params.get('no_girls_toilet', 'off') == 'on':
            schools = schools.annotate(
                girl_toilet_count=SumCase(
                    'yearlydata__toilet__count',
                    when='"schools_toilet"."type" = \'girl\''
                )
            )
            schools = schools.filter(girl_toilet_count=0)

        if params.get('needs_repair', 'off') == 'on':
            schools = schools.annotate(
                repair_count=SumCase(
                    'yearlydata__room__count',
                    when='"schools_room"."type" = \'class\' AND "schools_room"."condition" <> \'good\''
                )
            )
            schools = schools.filter(repair_count__gt=0)

        schools = schools[:limit]
        print schools.query
        # schools_json = serializers.serialize("json", schools)
        results = {
            'count': limit,
            'results': list(schools)
        }
        return self.render_to_response(results)
