# Generated by Django 2.0.4 on 2019-08-01 08:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pstate', '0014_auto_20190716_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='team',
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
    ]
