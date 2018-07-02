# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0003_notification_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='author',
            field=models.ForeignKey(related_name='notification_wrote', to=settings.AUTH_USER_MODEL),
        ),
    ]
