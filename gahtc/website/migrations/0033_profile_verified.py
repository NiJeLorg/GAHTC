# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0032_auto_20161031_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verified',
            field=models.NullBooleanField(default=None),
        ),
    ]
