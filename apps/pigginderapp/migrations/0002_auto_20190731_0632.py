# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-31 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pigginderapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relationship',
            name='description',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='relationship_goal',
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='relationship_goal',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
