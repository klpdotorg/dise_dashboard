from django.conf.urls import patterns, include, url
from schools.olap_views import OLAPEndPoint

urlpatterns = patterns('',
    url(r'^olap/$', OLAPEndPoint.as_view(), name='olap_endpoint'),
)
