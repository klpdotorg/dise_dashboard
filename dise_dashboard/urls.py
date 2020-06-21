from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

from schools.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

    url(r'^api/', include('dise_dashboard.api_urls')),

    path(r'admin/', admin.site.urls),
    url(r'^grappelli/', include('grappelli.urls')),
    #url(r'^explorer/', include('explorer.urls')),
]
