from django.views.generic import View, FormView, TemplateView
from django.db.models import Count, Min, Sum, Avg, F
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
        query = {}

        if params.get('year', ''):
            query['yearlydata__academic_year_id'] = params.get('year', '')

        if params.get('area_type', ''):
            query['yearlydata__area_type'] = params.get('area_type', '')

        if params.get('management', ''):
            if params.get('management') == 'govt':
                query['yearlydata__management_id__in'] = [1, 7]
            elif params.get('management') == 'pvt':
                query['yearlydata__management_id__in'] = [2, 3, 4, 5, 6, 8, 9, 97, 98]

        if params.get('no_electricity', ''):
            query['yearlydata__electricity_status'] = search_choices(YESNO, 'No')

        if params.get('no_library', ''):
            query['yearlydata__library_available'] = search_choices(YESNO, 'No')

        if params.get('no_ramp', ''):
            query['yearlydata__ramp_available'] = search_choices(YESNO, 'No')

        if params.get('no_playground', ''):
            query['yearlydata__playground_available'] = search_choices(YESNO, 'No')

        if params.get('no_medical', ''):
            query['yearlydata__medical_checkup'] = search_choices(YESNO, 'No')

        if params.get('no_room_hm', ''):
            query['yearlydata__room_for_headmaster'] = search_choices(YESNO, 'No')

        if params.get('no_water', ''):
            # 5 should be the id of "None" source
            # using `id` because it's indexed
            query['yearlydata__drinking_water_source_id'] = 5

        # All the non-aggregation non-annotation queries go above this
        schools = schools.filter(**query)

        if params.get('no_toilet', 'off') == 'on':
            schools = schools.annotate(total_toilets=Sum('yearlydata__toilet__count'))
            schools = schools.filter(total_toilets=0)

        if params.get('girl_boy_ratio', 'off') == 'on':
            schools = schools.annotate(
                total_girls=Sum('yearlydata__enrolment__total_girls'),
                total_boys=Sum('yearlydata__enrolment__total_boys'),
            )
            schools = schools.extra(
                where=[
                    '"total_boys" > 0',
                    '"total_girls" < "total_boys"'
                ]
            )

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
            schools = schools.filter(repair_count__gt=0).order_by('-repair_count')

        schools = schools[:limit]
        print schools.query
        # schools_json = serializers.serialize("json", schools)
        results = {
            'results': list(schools)
        }
        return self.render_to_response(results)
