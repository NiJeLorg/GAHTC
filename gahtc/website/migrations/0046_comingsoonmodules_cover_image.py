# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-25 04:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0045_auto_20170717_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='comingsoonmodules',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to=b'module_cover/%Y_%m_%d_%h_%M_%s'),
        ),
    ]
