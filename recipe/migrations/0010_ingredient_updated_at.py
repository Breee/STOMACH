# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-22 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_auto_20170613_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]