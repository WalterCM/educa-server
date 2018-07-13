# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0013_classroom_squedule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classroom',
            old_name='squedule',
            new_name='schedule',
        ),
    ]
