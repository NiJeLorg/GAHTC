# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_lectures_presentation_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectures',
            name='title',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='modules',
            name='authors',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='modules',
            name='title',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
