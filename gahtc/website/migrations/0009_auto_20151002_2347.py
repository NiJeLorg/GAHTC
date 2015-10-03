# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20150930_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='moduleDocuments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('document', models.FileField(null=True, upload_to=b'module_docs/%Y_%m_%d_%h_%M_%s', blank=True)),
                ('document_contents', models.TextField(default=b'', null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='modules',
            name='overview',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='overview_contents',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='syllabus',
        ),
        migrations.RemoveField(
            model_name='modules',
            name='syllabus_contents',
        ),
        migrations.AddField(
            model_name='moduledocuments',
            name='module',
            field=models.ForeignKey(to='website.modules'),
        ),
    ]
