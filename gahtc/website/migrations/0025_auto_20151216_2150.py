# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0024_lecturesegments_updated_lecture_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='language',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(related_name='userProfile', to=settings.AUTH_USER_MODEL),
        ),
    ]
