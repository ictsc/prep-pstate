from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from terraform_manager.models import TerraformFile, Environment


class TemplateModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProblemManager(models.Manager):

    def get_open_problem(self):
        # modeがOPEN状態で公開時間内の問題を抽出.
        queryset = self.filter(Q(mode='OPEN') | Q(mode='TIMER', start_date__lt=now(), end_date__gt=now())).order_by('id')
        return queryset


class Problem(TemplateModel):
    MODE_CHOICES = (
        ('OPEN', _('OPEN')),
        ('CLOSE', _('CLOSE')),
        ('TIMER', _('TIMER')),
    )

    objects = ProblemManager()

    name = models.CharField("問題名(管理用)", max_length=200)
    display_name = models.CharField("問題名(参加者向け)", max_length=200)
    description = models.TextField("問題文", blank=True, null=True)
    start_date = models.DateTimeField("問題公開日時", blank=True, null=True, default=now())
    end_date = models.DateTimeField("問題公開終了日時", blank=True, null=True, default=now())
    mode = models.CharField("公開モード", max_length=100, choices=MODE_CHOICES, default='CLOSE')
    is_enabled = models.BooleanField("公開フラグ", default=False)
    terraform_file_id = models.ForeignKey(TerraformFile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{} : {}'.format(self.name, self.display_name)

    def has_terraform_file(self):
        return self.terraform_file_id is not None


class ProblemEnvironment(TemplateModel):
    STATE_CHOICES = (
        ('IN_PREPARATION', _('IN_PREPARATION')),
        ('READY', _('READY')),
        ('IN_PROGRESS', _('IN_PROGRESS')),
        ('FINISH', _('FINISH')),
        ('WAITING_FOR_SCORING', _('WAITING_FOR_SCORING')),
        ('SCORING_HAS_ENDED', _('SCORING_HAS_ENDED')),
        ('WAITING_FOR_DELETE', _('WAITING_FOR_DELETE')),
        ('DELETED', _('DELETED')),

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
    team = models.ForeignKey("Team", on_delete=models.PROTECT, blank=True, null=True)
    participant = models.ForeignKey("Participant", on_delete=models.PROTECT, blank=True, null=True)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, null=True, related_name='problem_environment')
    problem = models.ForeignKey(Problem, related_name='problem_environment', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        problem_environment = ProblemEnvironment.objects.filter(id=self.id)
        if problem_environment.exists():
            message = "Change state"
            if "message" in kwargs and kwargs['message']:
                message = kwargs['message']
                del kwargs['message']
            ProblemEnvironmentLog(message=message,
                                  before_state=problem_environment[0].state,
                                  after_state=self.state,
                                  problem_environment=self).save()
        super(ProblemEnvironment, self).save(*args, **kwargs)

    @property
    def sorted_log_set(self):
        return self.logs.order_by('-created_at')


class ProblemEnvironmentLog(TemplateModel):
    message = models.TextField(blank=True, null=True)
    before_state = models.CharField(choices=ProblemEnvironment.STATE_CHOICES, max_length=100, blank=True, null=True)
    after_state = models.CharField(choices=ProblemEnvironment.STATE_CHOICES, max_length=100, blank=True, null=True)
    problem_environment = models.ForeignKey("ProblemEnvironment", related_name="logs", on_delete=models.CASCADE)


class User(AbstractUser):
    is_team = models.BooleanField(default=False)


class Team(User):
    team_name = models.CharField("チーム名", max_length=100)
    description = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    team_number = models.IntegerField(default=0, unique=True)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    def save(self, *args, **kwargs):
        self.is_team = True
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.username + " - " + self.team_name


class Participant(User):
    assign_team = models.ForeignKey("Team", verbose_name="所属チーム", related_name="participant",
                                    help_text="所属するチームを選択してください", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'


class Grade(TemplateModel):
    score = models.FloatField()
    team = models.ForeignKey("Team", blank=True, null=True, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, blank=True, null=True, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

class Github(TemplateModel):
    git_source = models.CharField(max_length=200, blank=False,
        help_text=_("git://github.com:sample/sample.git"),
        verbose_name=_('git source'))
    ssh_private_key = models.TextField(blank=True,
        verbose_name=_('SSH private key'))
    project_root_path = models.CharField(max_length=200, blank=True, default ="ictsc2019", 
        help_text=_("ictscXXXX"))
    teams_file = models.CharField(max_length=200, default="teams.yml")


