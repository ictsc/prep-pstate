from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class TemplateModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Problem(TemplateModel):
    name = models.CharField("問題名(管理用)", max_length=200)
    display_name = models.CharField("問題名(参加者向け)", max_length=200)
    description = models.TextField("問題文")
    start_date = models.DateTimeField("問題公開日時", blank=True, null=True)
    end_date = models.DateTimeField("問題公開終了日時", blank=True, null=True)
    is_enabled = models.BooleanField("公開フラグ", default=False)
    #   TODO    :   terraform-managerのコードをpstateに持ってきたら下のコメントアウトを外す.
    # terraform_file_id = models.ForeignKey('TerraformFile')


class ProblemEnvironment(TemplateModel):
    STATE_CHOICES = (
        ('IN_PREPARATION', 'IN_PREPARATION'),
        ('READY', 'READY'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('FINISH', 'FINISH'),
        ('WAITING_FOR_SCORING', 'WAITING_FOR_SCORING'),
        ('WAITING_FOR_DELETE', 'WAITING_FOR_DELETE'),
        ('DELETED', 'DELETED'),

    )

    vnc_server_ipv4_address = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True)
    vnc_server_port = models.CharField(max_length=5, blank=True, null=True)
    vnc_server_username = models.CharField(max_length=50, blank=True, null=True)
    vnc_server_password = models.CharField(max_length=50, blank=True, null=True)
    is_enabled = models.BooleanField("有効フラグ", default=False)
    state = models.CharField(choices=STATE_CHOICES, default='IN_PREPARATION')
    team = models.ForeignKey(Team)
    participant = models.ForeignKey(Participant)
    #   TODO    :   terraform-managerのコードをpstateに持ってきたら下のコメントアウトを外す.
    # environment = models.ForeignKey(Environment)
    problem = models.ForeignKey(Problem)


class Team(AbstractBaseUser):
    team_name = models.CharField(max_length=100)
    description = models.TextField()
    remarks = models.TextField()


class Participant(AbstractBaseUser):
    team = models.ForeignKey(Team, blank=True, null=True)


class Grade(TemplateModel):
    score = models.FloatField()
    team = models.ForeignKey(Team, blank=True, null=True)
    participant = models.ForeignKey(Participant, blank=True, null=True)
    problem = models.ForeignKey(Problem)
