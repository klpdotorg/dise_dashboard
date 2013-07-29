from django.views.generic import View, FormView, TemplateView
from django.db.models import Count, Min, Sum, Avg

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
        yearly_data = School.objects.values('code', 'name', 'pincode')

        if params.get('no_toilet', 'off') == 'on':
            yearly_data = yearly_data.annotate(total_toilets=Sum('yearlydata__toilet__count'))
            query['total_toilets'] = 0

        yearly_data = yearly_data.filter(**query).order_by('id')[:limit]

        return self.render_to_response(list(yearly_data))
