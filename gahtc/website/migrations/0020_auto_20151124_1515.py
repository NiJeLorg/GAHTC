# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_date_extensions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_auto_20151124_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lectures',
            name='maxdate',
            field=django_date_extensions.fields.ApproximateDateField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lectures',
            name='mindate',
            field=django_date_extensions.fields.ApproximateDateField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lecturesegments',
            name='maxdate',
            field=django_date_extensions.fields.ApproximateDateField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lecturesegments',
            name='mindate',
            field=django_date_extensions.fields.ApproximateDateField(max_length=10, null=True, blank=True),
        ),
    ]
