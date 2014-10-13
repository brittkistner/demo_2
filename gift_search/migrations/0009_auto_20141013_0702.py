# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gift_search', '0008_auto_20141012_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='link',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='wordreceiver',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
