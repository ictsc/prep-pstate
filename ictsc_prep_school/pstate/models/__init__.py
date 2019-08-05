import django
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
        queryset = self.filter(Q(mode='OPEN') | Q(mode='TIMER', start_date__lt=now(), end_date__gt=now())).order_by(
            'id')
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
    start_date = models.DateTimeField("問題公開日時", blank=True, null=True, default=django.utils.timezone.now)
    end_date = models.DateTimeField("問題公開終了日時", blank=True, null=True, default=django.utils.timezone.now)
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
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, null=True,
                                    related_name='problem_environment')
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

class Github(TemplateModel):
    name = models.CharField(max_length=100, default="ictsc-problems")
    git_source = models.CharField(max_length=200, blank=False,
        help_text=_("git://github.com:sample/sample.git"),
        verbose_name=_('git source'))
    ssh_private_key = models.TextField(blank=True,
        verbose_name=_('SSH private key'))
    project_root_path = models.CharField(max_length=200, blank=True, default ="ictsc2019", 
        help_text=_("ictscXXXX"))
    teams_file = models.CharField(max_length=200, default="teams.yml")
    problem_path = models.CharField(max_length=200, blank=True, default ="q1", 
        help_text=_("問題コードのディレクトリが保存されている場所。予選1ならq1"))

    def __str__(self):
        return self.name


class NotificationQueue(TemplateModel):
    MUTATION_TEMPLATE_ADD_PROBLEM_ENV = '''
    mutation {
        applyProblemEnvironment(input: {
            problemCode: "PROBLEM_CODE", teamNumber: TEAM_NUMBER,
            status: "STATUS", host: "HOST",
            user: "USER", password: "PASSWORD" }
        ) {
          problemEnvironment { id  }
      }
    }
    '''
    environment = models.ForeignKey(Environment, related_name="notification_queue", on_delete=models.CASCADE)
    payload = models.TextField()

    def save(self, *args, **kwargs):
        if len(self.environment.problem_environment.all()) != 1:
            raise Exception("InvalidData")
        problem_environment = self.environment.problem_environment.all().first()
        problem_name = problem_environment.problem.name
        try:
            team_number = problem_environment.team.team_number
        except:
            team_number = -1
        ipv4_address = problem_environment.vnc_server_ipv4_address
        username = problem_environment.vnc_server_username
        password = problem_environment.vnc_server_password
        status = str(self.environment.state)

        payload = self.MUTATION_TEMPLATE_ADD_PROBLEM_ENV

        if problem_name:
            payload = payload.replace("PROBLEM_CODE", problem_name)
        else:
            payload = payload.replace("PROBLEM_CODE", "")

        if team_number:
            payload = payload.replace("TEAM_NUMBER", str(team_number))
        else:
            payload = payload.replace("TEAM_NUMBER", "")

        if status:
            payload = payload.replace("STATUS", status)
        else:
            payload = payload.replace("STATUS", "")

        if ipv4_address:
            payload = payload.replace("HOST", ipv4_address)
        else:
            payload = payload.replace("HOST", "")

        if username:
            payload = payload.replace("USER", username)
        else:
            payload = payload.replace("USER", "")

        if password:
            payload = payload.replace("PASSWORD", password)
        else:
            payload = payload.replace("PASSWORD", "")
        self.payload = payload
        super(NotificationQueue, self).save(*args, **kwargs)
