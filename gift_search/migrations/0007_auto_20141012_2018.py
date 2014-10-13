# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gift_search', '0006_product_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiver',
            name='name',
            field=models.TextField(),
        ),
    ]
