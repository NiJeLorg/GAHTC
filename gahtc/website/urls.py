"""website URL Configuration
"""
from django.conf.urls import include, url
from website import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
