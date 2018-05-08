# Generated by Django 2.0.4 on 2018-05-07 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pstate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='assign_team',
            field=models.ForeignKey(blank=True, help_text='所属するチームを選択してください', null=True, on_delete=False, related_name='participant', to='pstate.Team', verbose_name='所属チーム'),
        ),
    ]