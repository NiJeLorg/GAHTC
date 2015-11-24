# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_auto_20151120_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='bundleLectureSegments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bundle', models.ForeignKey(to='website.bundles')),
                ('lectureSegment', models.ForeignKey(to='website.lectureSegments')),
            ],
        ),
    ]
