# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0028_lecturedocumentscomments_lecturescomments_lecturesegmentscomments_lectureslidescomments_moduledocume'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moduledocumentscomments',
            name='moduleDocument',
        ),
        migrations.RemoveField(
            model_name='moduledocumentscomments',
            name='user',
        ),
        migrations.DeleteModel(
            name='moduleDocumentsComments',
        ),
    ]
