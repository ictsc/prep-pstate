# Generated by Django 2.0.4 on 2018-05-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terraform_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variable',
            name='value',
            field=models.TextField(blank=True, null=True),
        ),
    ]
