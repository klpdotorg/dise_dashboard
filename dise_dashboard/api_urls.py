from django.conf.urls import patterns, url
from schools.api_views import (
    SchoolListView, SchoolInfoView, AggregationListView)


urlpatterns = patterns(
    '',
    url(r'^$', 'schools.api_views.api_root', name='api_root'),
    url(r'^(?P<session>[\d\-]{5})/school/$', SchoolListView.as_view(), name='api_school_list'),
    url(r'^(?P<session>[\d\-]{5})/school/(?P<dise_code>[\w]+)/$', SchoolInfoView.as_view(), name='api_school_info'),

    url(r'^(?P<session>[\d\-]{5})/(?P<entity>(cluster|block|district|assembly|parliament|pincode))/$', AggregationListView.as_view(), name='api_entity_list'),
)