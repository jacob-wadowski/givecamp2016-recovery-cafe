# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-25 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timecard', '0009_merge_20161016_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='punchtime',
            name='adminCheckoutTime',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='punchtime',
            name='isAdminCheckout',
            field=models.NullBooleanField(),
        ),
    ]