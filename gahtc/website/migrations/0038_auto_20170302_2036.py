# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0037_comingsoonmodules'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='institution_address',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='institution_city',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='institution_country',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='institution_postal_code',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
