# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 14:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_parser', '0010_postdata_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdata',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
