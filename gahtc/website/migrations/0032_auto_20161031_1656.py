# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0031_auto_20160323_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='instutution_document',
            field=models.FileField(default=b'', null=True, upload_to=b'insitution_docs/%Y_%m_%d_%h_%M_%s', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='member',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='website',
            field=models.URLField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
