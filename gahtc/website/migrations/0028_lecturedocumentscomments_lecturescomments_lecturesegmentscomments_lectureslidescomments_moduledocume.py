# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0027_auto_20151217_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='lectureDocumentsComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lectureDocument', models.ForeignKey(to='website.lectureDocuments')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='lecturesComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lecture', models.ForeignKey(to='website.lectures')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='lectureSegmentsComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lectureSegment', models.ForeignKey(to='website.lectureSegments')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='lectureSlidesComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lectureSlide', models.ForeignKey(to='website.lectureSlides')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='moduleDocumentsComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('moduleDocument', models.ForeignKey(to='website.moduleDocuments')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='modulesComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('module', models.ForeignKey(to='website.modules')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
