from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from schools.views import SearchView

urlpatterns = patterns('',
    url(r'^$', SearchView.as_view(), name='search'),

    # url(r'^schools/', include('schools.urls')),

    url(r'^api/v1/', include('schools.v1_urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)
