# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('website', '0020_auto_20151124_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='lectureSlidesSegment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slide', models.ImageField(null=True, upload_to=b'presentation_slides/%Y_%m_%d_%h_%M_%s', blank=True)),
                ('slide_number', models.IntegerField(default=0, null=True, blank=True)),
                ('extracted', models.BooleanField(default=False)),
                ('lecture_segment', models.ForeignKey(related_name='lectureSlidesLectureSegment', to='website.lectureSegments')),
                ('tags', taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
        ),
    ]
