# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('room', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('classes_done', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('overview', models.TextField()),
                ('image', models.FileField(upload_to='images')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='CourseInClassroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('classroom', models.ForeignKey(to='classrooms.Classroom')),
                ('course', models.ForeignKey(to='classrooms.Course')),
                ('professor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentInClassroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('classes_attended', models.PositiveIntegerField(default=0)),
                ('classroom', models.ForeignKey(to='classrooms.Classroom')),
            ],
        ),
        migrations.CreateModel(
            name='StudentInCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('pc1', models.PositiveIntegerField(default=0)),
                ('pc2', models.PositiveIntegerField(default=0)),
                ('pc3', models.PositiveIntegerField(default=0)),
                ('pc4', models.PositiveIntegerField(default=0)),
                ('midterm', models.PositiveIntegerField(default=0)),
                ('final', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(to='classrooms.CourseInClassroom')),
                ('student', models.ForeignKey(to='classrooms.StudentInClassroom')),
            ],
        ),
        migrations.AddField(
            model_name='studentinclassroom',
            name='courses',
            field=models.ManyToManyField(blank=True, to='classrooms.CourseInClassroom', through='classrooms.StudentInCourse'),
        ),
        migrations.AddField(
            model_name='studentinclassroom',
            name='student',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classroom',
            name='courses',
            field=models.ManyToManyField(blank=True, to='classrooms.Course', through='classrooms.CourseInClassroom'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, through='classrooms.StudentInClassroom'),
        ),
    ]
