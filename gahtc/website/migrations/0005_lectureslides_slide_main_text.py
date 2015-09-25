# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_lectures_extracted'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectureslides',
            name='slide_main_text',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
    ]
