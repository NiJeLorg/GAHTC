# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-22 11:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0047_merge_20170805_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturedocuments',
            name='doc_type',
            field=models.ForeignKey(blank=True, default=b'', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lecture_doc_type', to='website.docType'),
        ),
        migrations.AlterField(
            model_name='moduledocuments',
            name='doc_type',
            field=models.ForeignKey(blank=True, default=b'', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='module_doc_type', to='website.docType'),
        ),
    ]
