from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class Course(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    image = models.FileField(upload_to='images')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Classroom(models.Model):
    room = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    courses = models.ManyToManyField(Course,
                                    through='CourseInClassroom',
                                    blank=True)
    students = models.ManyToManyField(User,
                                      through='StudentInClassroom',
                                      blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.room


class CourseInClassroom(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    classes_done = models.PositiveIntegerField(default=0)

    professor = models.ForeignKey(User)


class StudentInClassroom(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    courses = models.ManyToManyField(CourseInClassroom, through='StudentInCourse', blank=True)


class StudentInCourse(models.Model):
    student = models.ForeignKey(StudentInClassroom, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseInClassroom, on_delete=models.CASCADE)

    classes_attended = models.PositiveIntegerField(default=0)

    pc1 = models.PositiveIntegerField(default=0)
    pc2 = models.PositiveIntegerField(default=0)
    pc3 = models.PositiveIntegerField(default=0)
    pc4 = models.PositiveIntegerField(default=0)
    midterm = models.PositiveIntegerField(default=0)
    final = models.PositiveIntegerField(default=0)


class Attachment(models.Model):
    course = models.ForeignKey(CourseInClassroom, related_name='attachment_added')
    created = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, related_name='attachment_uploaded')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="attachments", blank=True)

    class Meta:
        ordering = ('-created',)

class Notification(models.Model):
    course = models.ForeignKey(CourseInClassroom, related_name='notifications_created')
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='notification_wrote')
    subject = models.CharField(max_length=200)
    text = models.TextField(max_length=500)

    class Meta:
        ordering = ('-created',)

class Parent(User):
    students = models.ManyToManyField(User, related_name='student_added', blank=True)
