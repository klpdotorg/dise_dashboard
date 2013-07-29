from django.conf.urls import patterns, include, url
from schools.v1_views import V1SearchView

urlpatterns = patterns('',
    url(r'^search/$', V1SearchView.as_view(), name='v1_search'),
)
