from django.conf.urls import patterns, include, url
from schools.olap_views import OLAPEndPoint, OLAPUnifiedSearch
from schools.v1_views import V1SearchView

urlpatterns = patterns('',
    url(r'^olap/$', OLAPEndPoint.as_view(), name='olap_endpoint'),
    url(r'^olap/search/$', OLAPUnifiedSearch.as_view(), name='olap_unified_search'),
    url(r'^oltp/$', V1SearchView.as_view(), name='v1_search'),
)
