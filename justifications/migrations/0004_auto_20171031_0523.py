# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 05:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justifications', '0003_auto_20171031_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='evidence',
            name='correct',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='paperinteraction',
            name='annotated',
            field=models.NullBooleanField(),
        ),
    ]
