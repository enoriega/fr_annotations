# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 05:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interactions',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('direction', models.IntegerField()),
            ],
            options={
                'db_table': 'Interactions',
                'managed': False,
            },


        ),
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('gid', models.TextField(primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'Participants',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('evidence', models.TextField()),
                ('controller_text', models.TextField()),
                ('controlled_text', models.TextField()),
                ('context', models.TextField()),
            ],
            options={
                'db_table': 'Evidence',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PaperInteraction',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('pmcid', models.TextField()),
                ('frequency', models.IntegerField()),
                ('interaction', models.ForeignKey(db_column='interaction', on_delete=django.db.models.deletion.DO_NOTHING, to='justifications.Interactions')),
            ],
            options={
                'db_table': 'Paper_Interaction',
                'managed': False
            },
        ),
        migrations.AddField(
            model_name='evidence',
            name='interaction',
            field=models.ForeignKey(db_column='interaction', on_delete=django.db.models.deletion.DO_NOTHING, related_name='paper_interaction_interaction', to='justifications.PaperInteraction'),
        ),
        migrations.AddField(
            model_name='evidence',
            name='pmcid',
            field=models.ForeignKey(db_column='pmcid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='paper_interaction_pmcid', to='justifications.PaperInteraction'),
        ),
    ]
