# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-10 14:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0022_auto_20181110_2231'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfans',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='userfans',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='userfans',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='fans',
        ),
        migrations.DeleteModel(
            name='UserFans',
        ),
    ]
