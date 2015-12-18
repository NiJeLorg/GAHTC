# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_lectureslidessegment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lectureslidessegment',
            name='tags',
        ),
        migrations.AddField(
            model_name='lecturesegments',
            name='maxslidenumber',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='lecturesegments',
            name='minslidenumber',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
