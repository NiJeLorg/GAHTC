# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('website', '0014_auto_20151119_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='lectureSegments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default=b'', max_length=255)),
                ('authors', models.CharField(default=b'', max_length=255)),
                ('description', models.TextField(default=b'', null=True, blank=True)),
                ('mindate', models.DateField(null=True, blank=True)),
                ('maxdate', models.DateField(null=True, blank=True)),
                ('presentation', models.FileField(null=True, upload_to=b'presentations/%Y_%m_%d_%h_%M_%s', blank=True)),
                ('presentation_text', models.TextField(default=b'', null=True, blank=True)),
                ('extracted', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='lecturedocuments',
            name='authors',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='lecturedocuments',
            name='description',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='lecturedocuments',
            name='title',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='lectures',
            name='description',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='lectures',
            name='maxdate',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='lectures',
            name='mindate',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='moduledocuments',
            name='authors',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='moduledocuments',
            name='description',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='moduledocuments',
            name='title',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='modules',
            name='description',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lecturedocuments',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='lectures',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='lectureslides',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='moduledocuments',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='modules',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='lecturesegments',
            name='lecture',
            field=models.ForeignKey(related_name='lectureSegments', to='website.lectures'),
        ),
        migrations.AddField(
            model_name='lecturesegments',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
