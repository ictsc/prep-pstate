from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

from terraform_manager.models import TerraformFile, Environment


class TemplateModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Problem(TemplateModel):
    name = models.CharField("問題名(管理用)", max_length=200)
    display_name = models.CharField("問題名(参加者向け)", max_length=200)
    description = models.TextField("問題文", blank=True, null=True)
    start_date = models.DateTimeField("問題公開日時", blank=True, null=True)
    end_date = models.DateTimeField("問題公開終了日時", blank=True, null=True)
    is_enabled = models.BooleanField("公開フラグ", default=False)
    terraform_file_id = models.ForeignKey(TerraformFile, on_delete=False, null=True)

    def __str__(self):
        return '{} : {}'.format(self.name, self.display_name)


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

    VNC_DEFAULT_USER_NAME = 'ubuntu'

    def generate_vnc_server_port():
        # import random
        # return str(random.randint(1025, 50000))
        # 5901固定、必要に応じてrandom生成を有効化する.
        return str(5901)

    def generate_vnc_server_password():
        import string
        import random
        import os
        length = 14
        chars = string.ascii_letters + string.digits
        random.seed = (os.urandom(1024))
        return ''.join(random.choice(chars) for i in range(length))

    vnc_server_ipv4_address = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True)
    vnc_server_port = models.CharField(max_length=5, blank=True, null=True, default=generate_vnc_server_port)
    vnc_server_username = models.CharField(max_length=50, blank=True, null=True, default=VNC_DEFAULT_USER_NAME)
    vnc_server_password = models.CharField(max_length=50, blank=True, null=True, default=generate_vnc_server_password)
    is_enabled = models.BooleanField("有効フラグ", default=False)
    state = models.CharField(choices=STATE_CHOICES, default='IN_PREPARATION', max_length=100)
    team = models.ForeignKey("Team", on_delete=False, blank=True, null=True)
    participant = models.ForeignKey("Participant", on_delete=False, blank=True, null=True)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey(Problem, on_delete=False)


class ProblemEnvironmentLog(TemplateModel):
    message = models.TextField(blank=True, null=True)
    before_state = models.CharField(choices=ProblemEnvironment.STATE_CHOICES, max_length=100, blank=True, null=True)
    after_state = models.CharField(choices=ProblemEnvironment.STATE_CHOICES, max_length=100, blank=True, null=True)
    problem_environment = models.ForeignKey("ProblemEnvironment", related_name="logs", on_delete=models.CASCADE)


class User(AbstractUser):
    is_team = models.BooleanField(default=False)


class Team(User):
    team_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    def save(self, *args, **kwargs):
        self.is_team = True
        super(Team, self).save(*args, **kwargs)


class Participant(User):
    assign_team = models.ForeignKey("Team", verbose_name="所属チーム", related_name="participant",
                                    help_text="所属するチームを選択してください", blank=True, null=True, on_delete=False)

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'


class Grade(TemplateModel):
    score = models.FloatField()
    team = models.ForeignKey("Team", blank=True, null=True, on_delete=False)
    participant = models.ForeignKey(Participant, blank=True, null=True, on_delete=False)
    problem = models.ForeignKey(Problem, on_delete=False)
