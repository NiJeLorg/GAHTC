# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='lectureDocuments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('document', models.FileField(null=True, upload_to=b'presentation_docs/%Y_%m_%d_%h_%M_%s', blank=True)),
                ('document_contents', models.TextField(default=b'', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='lectures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('presentation', models.FileField(null=True, upload_to=b'presentations/%Y_%m_%d_%h_%M_%s', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='lectureSlides',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('slide', models.ImageField(null=True, upload_to=b'presentation_slides/%Y_%m_%d_%h_%M_%s', blank=True)),
                ('slide_notes', models.TextField(default=b'', null=True, blank=True)),
                ('lecture', models.ForeignKey(to='website.lectures')),
            ],
        ),
        migrations.CreateModel(
            name='modules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('syllabus', models.FileField(null=True, upload_to=b'module_docs/%Y_%m_%d_%h_%M_%s', blank=True)),
                ('syllabus_contents', models.TextField(default=b'', null=True, blank=True)),
                ('overview', models.FileField(null=True, upload_to=b'module_docs/%Y_%m_%d_%h_%M_%s', blank=True)),
                ('overview_contents', models.TextField(default=b'', null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='lectures',
            name='module',
            field=models.ForeignKey(to='website.modules'),
        ),
        migrations.AddField(
            model_name='lecturedocuments',
            name='lecture',
            field=models.ForeignKey(to='website.lectures'),
        ),
    ]
