# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0031_auto_20160323_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='bundles',
            name='contact',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bundles',
            name='downloaded',
            field=models.BooleanField(default=False),
        ),
    ]
