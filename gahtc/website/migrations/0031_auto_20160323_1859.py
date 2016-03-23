# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0030_lectureslides_presentation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturedocuments',
            name='document',
            field=models.FileField(default=b'', upload_to=b'presentation_docs/%Y_%m_%d_%h_%M_%s'),
        ),
        migrations.AlterField(
            model_name='lectures',
            name='presentation',
            field=models.FileField(default=b'', upload_to=b'presentations/%Y_%m_%d_%h_%M_%s'),
        ),
        migrations.AlterField(
            model_name='lecturesegments',
            name='presentation',
            field=models.FileField(default=b'', upload_to=b'presentations/%Y_%m_%d_%h_%M_%s'),
        ),
        migrations.AlterField(
            model_name='moduledocuments',
            name='document',
            field=models.FileField(default=b'', upload_to=b'module_docs/%Y_%m_%d_%h_%M_%s'),
        ),
    ]
