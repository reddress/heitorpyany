from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^view_diary/$', views.view_diary,
                           name='view_diary'),
                       
                       url(r'^view_entry/(?P<entry_id>\d+)/$',
                           views.view_entry,
                           name='view_entry'),
                       
                       url(r'^add_entry/$', views.add_entry,
                           name='add_entry'),
                       
                       url(r'^list_entries/$', views.list_entries,
                           name='list_entries'),
                       
                       url(r'^list_feelings/$', views.list_feelings,
                           name='list_feelings'),
                       
                       url(r'^entry_added/$', views.entry_added,
                           name='entry_added'),

                       url(r'^feeling/(?P<feeling_id>\d+)/$',
                           views.entries_by_feeling,
                           name='entries_by_feeling'),

                       url(r'^graph/$', views.graph,
                           name='graph'),
                       
                       url(r'^search/$', views.search, name='search'),
                       )
