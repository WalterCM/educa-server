from django.contrib import admin
from .models import Course, Classroom, CourseInClassroom, StudentInClassroom, StudentInCourse#, Notification


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'overview']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['room', 'slug', 'created']
    list_filter = ['created']
    search_fields = ['room']
    prepopulated_fields = {'slug': ('room',)}

@admin.register(CourseInClassroom)
class CourseInClassroomAdmin(admin.ModelAdmin):
    list_display = ['course', 'classroom', 'classes_done']

@admin.register(StudentInClassroom)
class StudentInClassroomAdmin(admin.ModelAdmin):
	list_display = ['student', 'classroom']
    #prepopulated_fields = {'slug': ('room',)}

@admin.register(StudentInCourse)
class StudentInCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'pc1', 'pc2', 'pc3', 'pc4', 'midterm', 'final']

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['', 'subject', 'text']