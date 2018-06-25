import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Environment(models.Model):
    """
    Terraformの実行環境の情報を格納するモデル.
    """

    STATE_CHOICES = (
        ('IN_WAITING_FOR_START', _('IN_WAITING_FOR_START')),
        ('IN_FILE_COPYING', _('IN_FILE_COPYING')),
        ('IN_INITIALIZE', _('IN_INITIALIZE')),
        ('INITIALIZED', _('INITIALIZED')),
        ('IN_PLANNING', _('IN_PLANNING')),
        ('PLANNED', _('PLANNED')),
        ('IN_APPLYING', _('IN_APPLYING')),
        ('APPLIED', _('APPLIED')),
        ('IN_DESTROYING', _('IN_DESTROYING')),
        ('DESTROYED', _('DESTROYED')),
        ('FAILED', _('FAILED')),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terraform_file = models.ForeignKey('TerraformFile', unique=False, on_delete=models.SET_NULL, null=True, related_name='environment')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=_('IN_WAITING_FOR_START'))
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def sorted_log_set(self):
        return self.logs.order_by('-created_at')


class Log(models.Model):
    """
    Terraformの実行環境でコマンドを実行ログを格納するモデル.
    """

    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='logs')
    return_code = models.IntegerField(blank=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attribute(models.Model):
    """
    Terraformのproviderに紐づく属性をkey:value形式で格納するモデル.
    今のところ、さくらのクラウドを使うに必要な以下の情報を格納する.
    -   zone
    -   token
    -   secret
    """

    key = models.CharField(max_length=100)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)


class Provider(models.Model):
    """
    Terraformののprovider情報を格納するモデル.
    """

    name = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=100)
    attribute = models.ManyToManyField('Attribute', blank=True)

    def __str__(self):
        return self.name


class Variable(models.Model):
    """
    Terraformの実行時に変数を用いる場合に変数を格納するモデル.
    保存した変数は、variables.tfファイルとして以下の内容で出力されます.

    variable "key" { default = "value" }
    ...
    """

    key = models.CharField(max_length=100)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)


class ShellScript(models.Model):
    """
    さくらのクラウドのスタートアップスクリプト(ShellScript)を格納するモデル.
    サーバ内部の構築は、さくらのクラウドのスタートアップスクリプト機能を用いて行います.
    https://sacloud.github.io/terraform-provider-sakuracloud/configuration/resources/note/
    """

    name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    terraform_file = models.ForeignKey('TerraformFile', related_name='shell_script', unique=False, on_delete=models.CASCADE)


class TerraformFile(models.Model):
    """
    Terraformのtfファイルデータを格納するモデル.
    tfファイルと同時に、変数(variable)とプロバイダ(provider)も外部モデルとして保持する.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    body = models.TextField()
    file_name = models.CharField(max_length=200)
    variables = models.ManyToManyField('Variable', blank=True)
    provider = models.ForeignKey('Provider', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def has_shell_script(self):
        return 0 < self.shell_script.count()

    def has_variable(self):
        return 0 < self.variables.count()
