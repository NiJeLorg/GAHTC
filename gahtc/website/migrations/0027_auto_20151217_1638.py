# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0026_auto_20151217_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='autosubscribe',
            field=models.BooleanField(default=True, help_text='Automatically subscribe to topics that you answer', verbose_name='Automatically subscribe'),
        ),
        migrations.AddField(
            model_name='profile',
            name='post_count',
            field=models.IntegerField(default=0, verbose_name='Post count', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='show_signatures',
            field=models.BooleanField(default=True, verbose_name='Show signatures'),
        ),
        migrations.AddField(
            model_name='profile',
            name='signature',
            field=models.TextField(max_length=255, verbose_name='Signature', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='signature_html',
            field=models.TextField(max_length=255, verbose_name='Signature HTML Version', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='time_zone',
            field=models.FloatField(default=3.0, verbose_name='Time zone', choices=[(-12.0, b'-12'), (-11.0, b'-11'), (-10.0, b'-10'), (-9.5, b'-09.5'), (-9.0, b'-09'), (-8.5, b'-08.5'), (-8.0, b'-08 PST'), (-7.0, b'-07 MST'), (-6.0, b'-06 CST'), (-5.0, b'-05 EST'), (-4.0, b'-04 AST'), (-3.5, b'-03.5'), (-3.0, b'-03 ADT'), (-2.0, b'-02'), (-1.0, b'-01'), (0.0, b'00 GMT'), (1.0, b'+01 CET'), (2.0, b'+02'), (3.0, b'+03'), (3.5, b'+03.5'), (4.0, b'+04'), (4.5, b'+04.5'), (5.0, b'+05'), (5.5, b'+05.5'), (6.0, b'+06'), (6.5, b'+06.5'), (7.0, b'+07'), (8.0, b'+08'), (9.0, b'+09'), (9.5, b'+09.5'), (10.0, b'+10'), (10.5, b'+10.5'), (11.0, b'+11'), (11.5, b'+11.5'), (12.0, b'+12'), (13.0, b'+13'), (14.0, b'+14')]),
        ),
    ]
