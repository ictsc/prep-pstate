# Generated by Django 2.0.4 on 2019-07-16 06:23

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('terraform_manager', '0008_environment_tfstate'),
        ('pstate', '0014_auto_20190716_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payload', models.TextField()),
                ('environment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_queue', to='terraform_manager.Environment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]