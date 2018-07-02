# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('subject', models.CharField(max_length=200)),
                ('text', models.TextField(max_length=500)),
                ('course', models.ForeignKey(related_name='notifications_created', to='classrooms.CourseInClassroom')),
            ],
        ),
    ]
