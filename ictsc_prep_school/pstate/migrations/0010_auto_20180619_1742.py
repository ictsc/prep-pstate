# Generated by Django 2.0.4 on 2018-06-19 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pstate', '0009_auto_20180619_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemenvironment',
            name='environment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='problem_environment', to='terraform_manager.Environment'),
        ),
    ]
