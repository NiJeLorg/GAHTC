# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0035_auto_20161112_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='bundles',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 13, 18, 53, 58, 921265), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userlecturedownload',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 13, 18, 54, 10, 722997), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usermoduledownload',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 13, 18, 54, 13, 549657), auto_now_add=True),
            preserve_default=False,
        ),
    ]
