# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-09 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_parser', '0003_auto_20160809_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdata',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
