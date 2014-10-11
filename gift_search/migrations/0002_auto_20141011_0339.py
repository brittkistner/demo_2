# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gift_search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='receivers',
            field=models.ManyToManyField(default=None, related_name=b'products', through='gift_search.ProductReceiver', to=b'gift_search.Receiver'),
        ),
    ]
