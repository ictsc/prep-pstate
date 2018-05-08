# Generated by Django 2.0.4 on 2018-05-07 10:42

from django.db import migrations, models
import pstate.models


class Migration(migrations.Migration):

    dependencies = [
        ('pstate', '0003_auto_20180507_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemenvironment',
            name='participant',
            field=models.ForeignKey(blank=True, null=True, on_delete=False, to='pstate.Participant'),
        ),
        migrations.AlterField(
            model_name='problemenvironment',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=False, to='pstate.Team'),
        ),
        migrations.AlterField(
            model_name='problemenvironment',
            name='vnc_server_password',
            field=models.CharField(blank=True, default=pstate.models.ProblemEnvironment.generate_vnc_server_password, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='problemenvironment',
            name='vnc_server_port',
            field=models.CharField(blank=True, default=pstate.models.ProblemEnvironment.generate_vnc_server_port, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='problemenvironment',
            name='vnc_server_username',
            field=models.CharField(blank=True, default='ubuntu', max_length=50, null=True),
        ),
    ]
