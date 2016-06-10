# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-11 03:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plink', '0004_plink_pretty_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plinkoption',
            name='plink_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plink.Plink', unique=True),
        ),
    ]
