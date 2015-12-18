"""website URL Configuration
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from website import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^bundles/$', views.mybundles, name='mybundles'),
    url(r'^profile/$', views.myprofile, name='myprofile'),
    url(r'^searches/$', views.mysavedsearches, name='mysavedsearches'),
    url(r'^show_module/(?P<id>\d+)/$', views.showModule, name='showModule'),
    url(r'^show_lecture/(?P<id>\d+)/$', views.showLecture, name='showLecture'),
    url(r'^show_lecture_segment/(?P<id>\d+)/$', views.showLectureSegment, name='showLectureSegment'),
    url(r'^show_lecture_document/(?P<id>\d+)/$', views.showLectureDocument, name='showLectureDocument'),
    url(r'^show_lecture_slide/(?P<id>\d+)/$', views.showLectureSlide, name='showLectureSlide'),
    url(r'^show_lecture_modal/(?P<id>\d+)/$', views.showLectureModal, name='showLectureModal'),
    url(r'^show_lecture_segment_modal/(?P<id>\d+)/$', views.showLectureSegmentModal, name='showLectureSegmentModal'),
    url(r'^create_new_bundle/$', views.createNewBundle, name='createNewBundle'),
    url(r'^add_to_bundle/$', views.addToBundle, name='addToBundle'),
    url(r'^remove_from_bundle/$', views.removeFromBundle, name='removeFromBundle'),
    url(r'^show_bundle/(?P<id>\d+)/$', views.showBundle, name='showBundle'),
    url(r'^zip_up_bundle/(?P<id>\d+)/$', views.zipUpBundle, name='zipUpBundle'),
    url(r'^zip_up_module/(?P<id>\d+)/$', views.zipUpModule, name='zipUpModule'),
    url(r'^zip_up_lecture/(?P<id>\d+)/$', views.zipUpLecture, name='zipUpLecture'),
    url(r'^refresh_sidebar_bundle/$', views.refreshSidebarBundle, name='refreshSidebarBundle'),
    url(r'^update_profile/$', views.updateProfile, name='updateProfile'),
    url(r'^modules/$', views.modulesView, name='modulesView'),
    url(r'^lectures/$', views.lecturesView, name='lecturesView'),
    url(r'^members/$', views.membersView, name='membersView'),
    url(r'^save_search/$', views.saveSearchString, name='saveSearchString'),
    url(r'^save_comment/$', views.saveComment, name='saveComment'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^admin_module/$', views.admin_module, name='admin_module'),
    url(r'^admin_module/(?P<id>\d+)/$', views.admin_module, name='admin_module'),
    url(r'^admin_removemodule/(?P<id>\d+)/$', views.admin_removemodule, name='admin_removemodule'),
    url(r'^admin_moduledoc/$', views.admin_moduledoc, name='admin_moduledoc'),
    url(r'^admin_moduledoc/(?P<id>\d+)/$', views.admin_moduledoc, name='admin_moduledoc'),
    url(r'^admin_moduledoc/(?P<id>\d+)/(?P<moduleid>\d+)/$', views.admin_moduledoc, name='admin_moduledoc'),
    url(r'^admin_removemoduledoc/(?P<id>\d+)/$', views.admin_removemoduledoc, name='admin_removemoduledoc'),
    url(r'^admin_lecture/$', views.admin_lecture, name='admin_lecture'),
    url(r'^admin_lecture/(?P<id>\d+)/$', views.admin_lecture, name='admin_lecture'),
    url(r'^admin_lecture/(?P<id>\d+)/(?P<moduleid>\d+)/$', views.admin_lecture, name='admin_lecture'),
    url(r'^admin_removelecture/(?P<id>\d+)/$', views.admin_removelecture, name='admin_removelecture'),
    url(r'^admin_lecturesegment/$', views.admin_lecturesegment, name='admin_lecturesegment'),
    url(r'^admin_lecturesegment/(?P<id>\d+)/$', views.admin_lecturesegment, name='admin_lecturesegment'),
    url(r'^admin_lecturesegment/(?P<id>\d+)/(?P<lectureid>\d+)/$', views.admin_lecturesegment, name='admin_lecturesegment'),
    url(r'^admin_removelecturesegment/(?P<id>\d+)/$', views.admin_removelecturesegment, name='admin_removelecturesegment'),
    url(r'^admin_lecturedoc/$', views.admin_lecturedoc, name='admin_lecturedoc'),
    url(r'^admin_lecturedoc/(?P<id>\d+)/$', views.admin_lecturedoc, name='admin_lecturedoc'),
    url(r'^admin_lecturedoc/(?P<id>\d+)/(?P<lectureid>\d+)/$', views.admin_lecturedoc, name='admin_lecturedoc'),
    url(r'^admin_removelecturdoc/(?P<id>\d+)/$', views.admin_removelecturedoc, name='admin_removelecturedoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
