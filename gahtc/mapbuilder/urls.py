from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^startmap/$', views.startmap, name='startmap'),
    url(r'^map/$', views.map, name='map'),
    url(r'^map-extent/$', views.mapextent, name='map-extent'),
    url(r'^map-export/(?P<id>[0-9]+)$', views.mapexport, name='map-export'),
    url(r'^map-export/$', views.mapexport, name='map-export'),
    url(r'^mymaps/$', views.mymaps, name='mymaps'),
]