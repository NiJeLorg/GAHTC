# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_lectureslides_slide_main_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectures',
            name='authors',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
