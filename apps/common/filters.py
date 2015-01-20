from rest_framework import filters
from django.contrib.gis.geos import Polygon
from rest_framework.exceptions import ParseError


class KLPInBBOXFilter(filters.BaseFilterBackend):
    """
    Filter that only sends objects inside given bbox
    """
    bbox_param = 'bbox'

    def get_filter_bbox(self, request):
        bbox_string = request.QUERY_PARAMS.get(self.bbox_param, None)
        if not bbox_string:
            return None
        try:
            p1x, p1y, p2x, p2y = (float(n) for n in bbox_string.split(','))
        except ValueError:
            raise ParseError("Not valid bbox string in parameter %s."
                             % self.bbox_param)
        x = Polygon.from_bbox((p1x, p1y, p2x, p2y))
        return x

    def filter_queryset(self, request, queryset, view):
        filter_field = view.get_bbox_filter_field()

        bbox = self.get_filter_bbox(request)

        if not bbox:
            return queryset

        return queryset.filter(**{'{}__contained'.format(filter_field): bbox})


class TextSearchFilter(filters.BaseFilterBackend):
    """
    Filter that does text search in PK fields
    """
    text_param = 'text'

    def filter_queryset(self, request, queryset, view):
        text = request.GET.get('text', '')
        filters = {}

        if text:
            serializer = view.get_serializer_class()
            name_field = getattr(
                serializer.Meta, 'name_field',
                getattr(serializer.Meta, 'pk_field',)
            )

            filters['{}__icontains'.format(name_field)] = text

        return queryset.filter(**filters)
