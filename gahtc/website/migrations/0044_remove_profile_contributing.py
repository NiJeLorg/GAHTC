# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-07 21:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0043_auto_20170630_2220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='contributing',
        ),
    ]
