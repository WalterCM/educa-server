# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0004_auto_20180701_1703'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='notification',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 1, 17, 31, 53, 878978, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
