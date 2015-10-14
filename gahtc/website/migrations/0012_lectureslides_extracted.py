# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectureslides',
            name='extracted',
            field=models.BooleanField(default=False),
        ),
    ]
