# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classrooms', '0011_auto_20180707_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='students',
        ),
        migrations.AddField(
            model_name='parent',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='student_added', to=settings.AUTH_USER_MODEL),
        ),
    ]
