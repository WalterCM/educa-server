# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0002_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='author',
            field=models.CharField(verbose_name=django.contrib.auth.models.User, max_length=200, default='Walter'),
            preserve_default=False,
        ),
    ]
