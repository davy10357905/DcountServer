# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_parser', '0012_auto_20160902_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdata',
            name='updated_at',
            field=models.CharField(default='no updated yet', max_length=255),
        ),
    ]
