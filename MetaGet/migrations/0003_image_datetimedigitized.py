# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-01 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MetaGet', '0002_image_md5sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='DateTimeDigitized',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
