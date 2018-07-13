# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0012_auto_20180707_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='squedule',
            field=models.FileField(default='', upload_to='squedules'),
            preserve_default=False,
        ),
    ]
