from django.conf.urls import url, include
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^token/$', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/$', views.MyTokenRefreshView.as_view(), name='token_refresh'),
    url(r'^register/$', views.UserRegisterView.as_view(), name='register'),

    # url(r'^courses/$', views.CourseListView.as_view(), name='course_list'),
    # url(r'^courses/(?P<pk>\d+)/$', views.CourseDetailView.as_view(), name='course_detail'),
    url(r'^mine/$', views.MineView.as_view(), name='my_courses_list'),
    url(r'^notmine/$', views.NotmineView.as_view(), name='enrollment_list'),
    # url(r'^classrooms/create/$', views.ClassroomCreateView.as_view(), name='classroom_create'),
    url(r'^classrooms/(?P<classroom_id>\d+)/enroll/$', views.ClassroomEnrollView.as_view(), name='classroom_enroll'),
    url(r'^classrooms/(?P<classroom_id>\d+)/courses/$', views.CoursesFromClassroomView.as_view(), name='course_list'),
    url(r'^classrooms/(?P<classroom_id>\d+)/courses/(?P<course_id>\d+)/attendance/$', views.StudentsAttendanceView.as_view(), name='class_attendance'),
    url(r'^classrooms/(?P<classroom_id>\d+)/courses/(?P<course_id>\d+)/grades/$', views.StudentsGradesView.as_view(), name='class_grades'),
    url(r'^classrooms/(?P<classroom_id>\d+)/courses/(?P<course_id>\d+)/attachments/$', views.StudentsAttachmentsView.as_view(), name='class_attachments'),
    url(r'^classrooms/(?P<classroom_id>\d+)/courses/(?P<course_id>\d+)/notifications/$', views.StudentsNotificationsView.as_view(), name='class_notifications'),
]
