# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0010_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='students',
            field=models.ForeignKey(blank=True, related_name='student_added', to=settings.AUTH_USER_MODEL),
        ),
    ]
