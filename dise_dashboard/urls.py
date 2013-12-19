from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from schools.views import HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),

    # url(r'^schools/', include('schools.urls')),

    url(r'^api/v1/', include('schools.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)
