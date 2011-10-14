from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'mm_core/main.html'}),
)