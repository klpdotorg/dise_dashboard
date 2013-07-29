from django.conf.urls import patterns, include, url
from .views import SearchView

urlpatterns = patterns('',
    url(r'^search/$', SearchView.as_view(), name='search'),
)
