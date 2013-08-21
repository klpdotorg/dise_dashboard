from django.views.generic import View, FormView, TemplateView
from django.db.models import Count, Min, Sum, Avg, F, Q
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json
from django.core import serializers

from common import SumCase
from common.views import JSONResponseMixin
from schools.models import YearlyData, School, SchoolManaagement,\
DrinkingWaterSource, BoundaryWallType, search_choices, YESNO, MDM_STATUS


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
                govt_mgmt = SchoolManaagement.objects.filter(
                    Q(name__iexact='Department of Education') |
                    Q(name__iexact='Central Govt.')
                )
                query['yearlydata__management_id__in'] = govt_mgmt
            elif params.get('management') == 'pvt':
                pvt_mgmt = SchoolManaagement.objects.exclude(
                    Q(name__iexact='Department of Education') |
                    Q(name__iexact='Central Govt.')
                )
                query['yearlydata__management_id__in'] = pvt_mgmt

        if params.get('no_electricity', ''):
            query['yearlydata__electricity_status'] = search_choices(YESNO, 'No')

        if params.get('no_secure_wall', ''):
            insecure_wall_types = BoundaryWallType.objects.exclude(name__iexact="Pucca")
            query['yearlydata__boundary_wall_type_id__in'] = insecure_wall_types

        if params.get('no_mdm', ''):
            query['yearlydata__middaymeal_status__in'] = [
                search_choices(MDM_STATUS, 'Not applicable'),
                search_choices(MDM_STATUS, 'Not provided'),
            ]

        if params.get('no_library', ''):
            query['yearlydata__library_available'] = search_choices(YESNO, 'No')

        if params.get('no_ramp', ''):
            query['yearlydata__ramp_available'] = search_choices(YESNO, 'No')

        if params.get('no_blackboard', ''):
            query['yearlydata__blackboard_count'] = 0

        if params.get('no_playground', ''):
            query['yearlydata__playground_available'] = search_choices(YESNO, 'No')

        if params.get('no_medical', ''):
            query['yearlydata__medical_checkup'] = search_choices(YESNO, 'No')

        if params.get('no_room_hm', ''):
            query['yearlydata__room_for_headmaster'] = search_choices(YESNO, 'No')

        if params.get('no_sdmc_constituted', ''):
            query['yearlydata__sdmc_constituted'] = search_choices(YESNO, 'No')

        if params.get('no_sdmc_meeting', ''):
            query['yearlydata__sdmc_meeting_count'] = 0

        if params.get('no_textbook', ''):
            query['yearlydata__textbook_received'] = search_choices(YESNO, 'No')

        if params.get('weakersec_children_enrolled', ''):
            query['yearlydata__weakersec_children_enrolled__gt'] = 0

        if params.get('no_water', ''):
            try:
                query['yearlydata__drinking_water_source'] = DrinkingWaterSource.objects.get(name__iexact="None")
            except:
                # 5 should be the id of "None" source
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
