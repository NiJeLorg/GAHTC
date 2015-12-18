# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_auto_20151208_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturesegments',
            name='updated_lecture_review',
            field=models.BooleanField(default=False),
        ),
    ]
