# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0025_auto_20151216_2150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='pic',
            new_name='avatar',
        ),
    ]
