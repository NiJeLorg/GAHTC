"""website URL Configuration
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from website import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^show_module/(?P<id>\d+)/$', views.showModule, name='showModule'),
    url(r'^show_lecture/(?P<id>\d+)/$', views.showLecture, name='showLecture'),
    url(r'^show_lecture_document/(?P<id>\d+)/$', views.showLectureDocument, name='showLectureDocument'),
    url(r'^show_lecture_slide/(?P<id>\d+)/$', views.showLectureSlide, name='showLectureSlide'),
    url(r'^create_new_bundle/$', views.createNewBundle, name='createNewBundle'),
    url(r'^add_to_bundle/$', views.addToBundle, name='addToBundle'),
    url(r'^remove_from_bundle/$', views.removeFromBundle, name='removeFromBundle'),
    url(r'^show_bundle/(?P<id>\d+)/$', views.showBundle, name='showBundle'),
    url(r'^zip_up_bundle/(?P<id>\d+)/$', views.zipUpBundle, name='zipUpBundle'),
    url(r'^refresh_sidebar_bundle/$', views.refreshSidebarBundle, name='refreshSidebarBundle'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
