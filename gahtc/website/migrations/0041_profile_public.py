# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-13 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0040_auto_20170415_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
