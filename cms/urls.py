from django.conf.urls import patterns, url
from cms.models import Story
from django.views.generic import ListView, DetailView

info_dict = {'queryset': Story.object.all(), 'template_object_name': 'story'}

urlpatterns = patterns('',
                       url(r'^(?P<slug>[-\w]+)/$', DetailView.as_view(), info_dict, name="cms-story"),
                       url(r'^$', ListView.as_view(), info_dict, name="cms-home"),
                       )

urlpatterns += patterns('cms.views',
                        url(r'^category/(?P<slug>[-\w]+)/$', 'category', name="cms-category"),
                        # url(r'^search/$', 'search', name="cms-search"),
                        )
