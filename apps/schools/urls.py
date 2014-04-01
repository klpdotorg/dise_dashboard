from django.conf.urls import patterns, include, url
from schools.olap_views import OLAPEndPoint, OLAPUnifiedSearch

urlpatterns = patterns('',
    url(r'^olap/$', OLAPEndPoint.as_view(), name='olap_endpoint'),
    url(r'^olap/search/$', OLAPUnifiedSearch.as_view(), name='olap_unified_search'),
)
