# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_auto_20151121_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturedocuments',
            name='authors',
        ),
        migrations.RemoveField(
            model_name='lecturesegments',
            name='authors',
        ),
        migrations.AddField(
            model_name='lecturedocuments',
            name='extracted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='moduledocuments',
            name='extracted',
            field=models.BooleanField(default=False),
        ),
    ]
