# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 19:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('justifications', '0007_auto_20171031_0631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evidence',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='paperinteraction',
            options={'managed': False},
        ),
    ]