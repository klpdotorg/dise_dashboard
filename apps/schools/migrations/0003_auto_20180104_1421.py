# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_auto_20171231_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='dise1011basicdata',
            name='academic_year',
            field=models.CharField(max_length=35, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dise1112basicdata',
            name='academic_year',
            field=models.CharField(max_length=35, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dise1213basicdata',
            name='academic_year',
            field=models.CharField(max_length=35, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dise1314basicdata',
            name='academic_year',
            field=models.CharField(max_length=35, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dise1415basicdata',
            name='academic_year',
            field=models.CharField(max_length=35, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dise1516basicdata',
            name='academic_year',
            field=models.CharField(max_length=35, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dise1617basicdata',
            name='academic_year',
            field=models.CharField(max_length=35, blank=True),
            preserve_default=True,
        ),
    ]
