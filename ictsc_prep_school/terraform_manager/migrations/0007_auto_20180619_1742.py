# Generated by Django 2.0.4 on 2018-06-19 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terraform_manager', '0006_auto_20180619_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='terraform_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='environment', to='terraform_manager.TerraformFile'),
        ),
    ]
