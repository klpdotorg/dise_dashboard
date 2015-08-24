from rest_framework import filters
from rest_framework_gis.filters import InBBoxFilter


class KLPInBBOXFilter(InBBoxFilter):
    """
    Filter that only sends objects inside given bbox
    """
    bbox_param = 'bbox'


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
