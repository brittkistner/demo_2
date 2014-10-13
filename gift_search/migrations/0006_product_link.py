# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gift_search', '0005_auto_20141012_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.TextField(default=None),
            preserve_default=True,
        ),
    ]
