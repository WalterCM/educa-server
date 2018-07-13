# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classrooms', '0015_notification_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='read',
        ),
        migrations.AddField(
            model_name='notification',
            name='readers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
