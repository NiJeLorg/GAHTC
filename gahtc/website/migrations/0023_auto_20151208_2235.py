# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0022_auto_20151208_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturesegments',
            name='maxslidenumber',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lecturesegments',
            name='minslidenumber',
            field=models.IntegerField(default=0),
        ),
    ]
