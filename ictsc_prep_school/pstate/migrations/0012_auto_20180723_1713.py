# Generated by Django 2.0.4 on 2018-07-23 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pstate', '0011_auto_20180722_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='mode',
            field=models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSE', 'CLOSE'), ('TIMER', 'TIMER')], default='CLOSE', max_length=100, verbose_name='公開モード'),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(max_length=100, verbose_name='チーム名'),
        ),
    ]
