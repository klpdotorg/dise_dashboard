from django.conf.urls import patterns, url, include
from schools.api_views import (
    SchoolListView, SchoolInfoView, SchoolInfraView, SchoolFinView,
    AggregationListView, AggregationInfoView, AggregationSchoolListView, 
    ClustersInBlockView, ClustersInDistrictView, BlocksInDistrictView, 
    OmniSearchApiView)


urlpatterns = patterns(
    '',
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^$', 'schools.api_views.api_root', name='api_root'),
    url(r'^(?P<session>[\d\-]{5})/search/$', OmniSearchApiView.as_view(), name='api_search'),
    url(r'^(?P<session>[\d\-]{5})/school/$', SchoolListView.as_view(), name='api_school_list'),
    url(r'^(?P<session>[\d\-]{5})/school/(?P<dise_code>[\w]+)/$', SchoolInfoView.as_view(), name='api_school_info'),
    url(r'^(?P<session>[\d\-]{5})/school/(?P<dise_code>[\w]+)/infrastructure/$', SchoolInfraView.as_view(), name='api_school_infra'),
    url(r'^(?P<session>[\d\-]{5})/school/(?P<dise_code>[\w]+)/finance/$', SchoolFinView.as_view(), name='api_school_fin'),

    url(r'^(?P<session>[\d\-]{5})/(?P<entity>(cluster|block|district|assembly|parliament|pincode))/$', AggregationListView.as_view(), name='api_entity_list'),
    url(r'^(?P<session>[\d\-]{5})/(?P<entity>(cluster|block|district|assembly|parliament|pincode))/(?P<slug>[^\/]+)/$', AggregationInfoView.as_view(), name='api_entity_info'),
    url(r'^(?P<session>[\d\-]{5})/(?P<entity>(cluster|block|district|assembly|parliament|pincode))/(?P<slug>[^\/]+)/schools/$', AggregationSchoolListView.as_view(), name='api_entity_school_list'),

    url(r'^(?P<session>[\d\-]{5})/(?P<entity>block)/(?P<block_slug>[^\/]+)/clusters/$', ClustersInBlockView.as_view(), name='api_clusters_in_block'),
    url(r'^(?P<session>[\d\-]{5})/(?P<entity>district)/(?P<district_slug>[^\/]+)/clusters/$', ClustersInDistrictView.as_view(), name='api_clusters_in_district'),
    url(r'^(?P<session>[\d\-]{5})/(?P<entity>district)/(?P<district_slug>[^\/]+)/blocks/$', BlocksInDistrictView.as_view(), name='api_blocks_in_district'),
)
