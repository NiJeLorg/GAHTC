# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-10 11:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapbuilder', '0002_auto_20180509_2212'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Maps',
            new_name='Map',
        ),
    ]