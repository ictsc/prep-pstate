# Generated by Django 2.0.4 on 2019-07-16 02:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pstate', '0012_auto_20180723_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_number',
            field=models.IntegerField(default=0),
        ),
    ]
