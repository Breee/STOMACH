# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-12 11:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_auto_20170612_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ing_recipe',
            name='ing_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipe.Ingredient'),
        ),
        migrations.AlterField(
            model_name='ing_recipe',
            name='recipe_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipe.Recipe'),
        ),
    ]
