# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-07 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_empresa_cuentas_montadas'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoempresa',
            name='codigo',
            field=models.CharField(default='', max_length=65),
        ),
    ]
