# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0005_auto_20180701_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='classes_done',
        ),
        migrations.RemoveField(
            model_name='studentinclassroom',
            name='classes_attended',
        ),
        migrations.AddField(
            model_name='courseinclassroom',
            name='classes_done',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentincourse',
            name='classes_attended',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
