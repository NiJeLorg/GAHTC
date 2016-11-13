# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('website', '0036_auto_20161113_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='comingSoonModules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(default=b'', max_length=255)),
                ('authors', models.CharField(default=b'', max_length=255)),
                ('description', models.TextField(default=b'', null=True, blank=True)),
                ('tags', taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
        ),
    ]
