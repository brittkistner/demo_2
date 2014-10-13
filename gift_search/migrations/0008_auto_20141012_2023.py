# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gift_search', '0007_auto_20141012_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.TextField(null=True),
        ),
    ]
