# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0007_lectureslides_slide_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='bundleLecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='bundleLectureDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='bundleLectureSlides',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='bundleModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='bundles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bundlemodule',
            name='bundle',
            field=models.ForeignKey(to='website.bundles'),
        ),
        migrations.AddField(
            model_name='bundlemodule',
            name='module',
            field=models.ForeignKey(to='website.modules'),
        ),
        migrations.AddField(
            model_name='bundlelectureslides',
            name='bundle',
            field=models.ForeignKey(to='website.bundles'),
        ),
        migrations.AddField(
            model_name='bundlelectureslides',
            name='lectureSlide',
            field=models.ForeignKey(to='website.lectureSlides'),
        ),
        migrations.AddField(
            model_name='bundlelecturedocument',
            name='bundle',
            field=models.ForeignKey(to='website.bundles'),
        ),
        migrations.AddField(
            model_name='bundlelecturedocument',
            name='lectureDocument',
            field=models.ForeignKey(to='website.lectureDocuments'),
        ),
        migrations.AddField(
            model_name='bundlelecture',
            name='bundle',
            field=models.ForeignKey(to='website.bundles'),
        ),
        migrations.AddField(
            model_name='bundlelecture',
            name='lecture',
            field=models.ForeignKey(to='website.lectures'),
        ),
    ]
