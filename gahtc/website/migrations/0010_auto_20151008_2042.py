# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20151002_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectureslides',
            name='slide_notes_document',
            field=models.FileField(null=True, upload_to=b'slide_notes_docs/%Y_%m_%d_%h_%M_%s', blank=True),
        ),
        migrations.AlterField(
            model_name='lecturedocuments',
            name='lecture',
            field=models.ForeignKey(related_name='lectureDocsLecture', to='website.lectures'),
        ),
        migrations.AlterField(
            model_name='lectures',
            name='module',
            field=models.ForeignKey(related_name='lecturesModule', to='website.modules'),
        ),
        migrations.AlterField(
            model_name='lectureslides',
            name='lecture',
            field=models.ForeignKey(related_name='lectureSlidesLecture', to='website.lectures'),
        ),
        migrations.AlterField(
            model_name='moduledocuments',
            name='module',
            field=models.ForeignKey(related_name='moduleDocsModule', to='website.modules'),
        ),
    ]
