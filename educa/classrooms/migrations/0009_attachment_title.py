# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0008_auto_20180707_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='title',
            field=models.CharField(max_length=200, default='test'),
            preserve_default=False,
        ),
    ]
