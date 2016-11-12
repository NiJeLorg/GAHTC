# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0034_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='userLectureDownload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.BooleanField(default=False)),
                ('downloaded', models.BooleanField(default=False)),
                ('lecture', models.ForeignKey(to='website.lectures')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userModuleDownload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.BooleanField(default=False)),
                ('downloaded', models.BooleanField(default=False)),
                ('module', models.ForeignKey(to='website.modules')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='instutution_document',
            field=models.FileField(null=True, upload_to=b'insitution_docs/%Y_%m_%d_%h_%M_%s', blank=True),
        ),
    ]
