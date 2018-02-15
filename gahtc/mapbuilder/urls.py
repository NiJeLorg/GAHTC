from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^startmap/$', views.startmap, name='startmap'),
    url(r'^searchmap/$', views.searchmap, name='searchmap'),
]