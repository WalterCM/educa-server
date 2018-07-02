from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    url(r'^register/$', views.StudentRegistrationView.as_view(), name='student_registration'),
    url(r'^enroll-classroom/$', views.StudentEnrollClassroomView.as_view(), name='student_enroll_classroom'),
    url(r'^classrooms/$', views.StudentClassroomListView.as_view(), name='student_classroom_list'),
    url(r'^classroom/(?P<pk>\d+)/$',
        cache_page(60 * 15)(views.StudentClassroomDetailView.as_view()),
        name='student_classroom_detail'),
    url(r'^classroom/(?P<pk>\d+)/(?P<module_id>\d+)/$',
        cache_page(60 * 15)(views.StudentClassroomDetailView.as_view()),
        name='student_classroom_detail_module'),
]
