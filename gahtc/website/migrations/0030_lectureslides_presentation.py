# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0029_auto_20151217_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectureslides',
            name='presentation',
            field=models.FileField(null=True, upload_to=b'presentation_slides/%Y_%m_%d_%h_%M_%s', blank=True),
        ),
    ]
