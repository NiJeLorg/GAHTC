# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20150911_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectures',
            name='extracted',
            field=models.BooleanField(default=False),
        ),
    ]
