# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-10 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0019_remove_article_tage'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tage',
            field=models.ManyToManyField(to='repository.Tag'),
        ),
    ]
