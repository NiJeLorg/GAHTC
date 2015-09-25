# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_lectures_authors'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectureslides',
            name='slide_number',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
