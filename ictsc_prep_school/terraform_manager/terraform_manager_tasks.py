from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from python_terraform import Terraform

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ictsc_prep_school.settings.terraform_manager.develop')

app = Celery('terraform_manager')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

TERRAFORM_PATH = ''
TERRAFORM_ENVIRONMENT_ROOT_PATH = '/terraform-environment/'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


def get_app():
    return app


@app.task
def copy_tf_files(environment_id, terraform_file_id):
    """
    terraformの実行に必要なファイルをworkerのカレントディレクトリにコピーします.
    :param environment_id:  環境ID
    :param terraform_file_id:   terraformファイルID
    """
    prepare_environment(environment_id, terraform_file_id)


@app.task
def init(environment_id):
    """
    terraform initを実行します.
    :param environment_id:  環境ID
    """
    from pstate.models import NotificationQueue
    from terraform_manager.models import Environment
    environment = Environment.objects.get(id=environment_id)

    if not os.path.isdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + environment_id):
        prepare_environment(environment_id=environment_id, terraform_file_id=environment.terraform_file.id)
    environment.is_locked = True
    environment.state = 'IN_INITIALIZE'
    environment.save()
    NotificationQueue.objects.create(environment=environment)
    try:
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.init()
        save_log(environment_id, return_code, stdout, stderr)
    except:
        import traceback
        save_log(environment_id, 999, '', traceback.format_exc())
        environment.state = 'FAILED'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
    finally:
        environment.is_locked = False
        environment.state = 'INITIALIZED'
        environment.save()
        NotificationQueue.objects.create(environment=environment)


@app.task
def plan(environment_id, var):
    """
    terraform planを実行します.
    :param environment_id:  環境ID
    :param var: terraformコマンド実行時に引数に渡す変数
    """
    from pstate.models import NotificationQueue
    from terraform_manager.models import Environment
    environment = Environment.objects.get(id=environment_id)

    import os
    if not os.path.isdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + environment_id):
        prepare_environment(environment_id, environment.terraform_file.id)
        init(environment_id)
    if environment.is_locked:
        # ロックしているときはコマンドを実行しない.
        raise Exception()

    environment.is_locked = True
    environment.state = 'IN_PLANNING'
    environment.save()
    NotificationQueue.objects.create(environment=environment)
    try:
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.plan(var=var)
        save_log(environment_id, return_code, stdout, stderr)
    except:
        import traceback
        save_log(environment_id, 999, '', traceback.format_exc())
        environment.state = 'FAILED'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
    finally:
        environment.is_locked = False
        environment.state = 'PLANNED'
        environment.save()
        NotificationQueue.objects.create(environment=environment)


@app.task
def apply(environment_id, var):
    """
    terraform applyを実行します.
    :param environment_id:  環境ID
    :param var: terraformコマンド実行時に引数に渡す変数
    """
    FAILED_STATUS_CODE = [1, ]
    from pstate.models import NotificationQueue
    from terraform_manager.models import Environment
    environment = Environment.objects.get(id=environment_id)

    import os
    if not os.path.isdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + environment_id):
        prepare_environment(environment_id, environment.terraform_file.id)
        environment_dir = TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id)
        f = open(environment_dir + "/" + 'terraform.tfstate', 'wb')
        f.write(environment.tfstate.encode('utf-8'))
        f.close()
        init(environment_id)
    if environment.is_locked:
        # ロックしているときはコマンドを実行しない.
        raise Exception()

    environment.is_locked = True
    environment.state = 'IN_APPLYING'
    environment.save()
    NotificationQueue.objects.create(environment=environment)
    try:
        import os
        os.environ["TF_CLI_ARGS"] = "-parallelism=4 -auto-approve=true"
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.apply(var=var, skip_plan=True)
        os.environ.pop("TF_CLI_ARGS")
        save_log(environment_id, return_code, stdout, stderr)
        #   terraform output vnc_global_ip
        cmd = ['terraform', 'output', 'vnc_global_ip']
        import subprocess
        os.chdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code, stdout, stderr = result.returncode, result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
        save_log(environment_id, return_code, stdout, stderr)
        if return_code in FAILED_STATUS_CODE:
            raise Exception("terraformが異常終了したためtaskを停止します")

        from pstate.models import ProblemEnvironment
        problem_environment = ProblemEnvironment.objects.get(environment=environment)
        problem_environment.vnc_server_ipv4_address = stdout.strip()
        save_log(environment_id, return_code, stdout, stderr)
        if return_code in FAILED_STATUS_CODE:
            raise Exception("terraformが異常終了したためtaskを停止します")

        environment.state = 'APPLIED'
        environment.save()
        # TODO: 問題環境のstateが準備完了になるタイミングが一律同じでないためREADYに変更するタイミングの修正の可能性あり.
        problem_environment.state = 'READY'
        problem_environment.save()
        NotificationQueue.objects.create(environment=environment)
    except:
        import traceback
        save_log(environment_id, 999, '', traceback.format_exc())
        environment.state = 'FAILED'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
    else:
        environment.state = 'APPLIED'
        from pstate.models import ProblemEnvironment
        problem_environment = ProblemEnvironment.objects.get(environment=environment)
        problem_environment.state = 'READY'
        problem_environment.save()
    finally:
        environment.is_locked = False
        environment.save()
        NotificationQueue.objects.create(environment=environment)
        import subprocess
        # tfstateを保存.
        cmd_cat = ['cat', 'terraform.tfstate']
        result = subprocess.run(cmd_cat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code, stdout, stderr = result.returncode, result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
        environment.tfstate = stdout
        environment.save()


@app.task
def destroy(environment_id, var):
    """
    terraform destroyを実行します.
    :param environment_id:  環境ID
    :param var: terraformコマンド実行時に引数に渡す変数
    """
    FAILED_STATUS_CODE = [1, ]

    #   TODO    :   マルチノードの場合、正常に処理が実行されないので、backendを指定してステータスを管理する.
    from terraform_manager.models import Environment
    environment = Environment.objects.get(id=environment_id)
    from pstate.models import NotificationQueue

    import os
    if not os.path.isdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + environment_id):
        prepare_environment(environment_id, environment.terraform_file.id)
        environment_dir = TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id)
        f = open(environment_dir + "/" + 'terraform.tfstate', 'wb')
        f.write(environment.tfstate.encode('utf-8'))
        f.close()
        init(environment_id)
    if environment.is_locked:
        # ロックしているときはコマンドを実行しない.
        raise Exception()

    environment.is_locked = True
    environment.state = 'IN_DESTROYING'
    environment.save()
    NotificationQueue.objects.create(environment=environment)
    try:
        import os
        os.environ["TF_CLI_ARGS"] = "-parallelism=4 -auto-approve=true"
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.destroy(var=var, force=True)
        os.environ.pop("TF_CLI_ARGS")
        save_log(environment_id, return_code, stdout, stderr)
        if return_code in FAILED_STATUS_CODE:
            raise Exception("terraformが異常終了したためtaskを停止します")
    except:
        import traceback
        save_log(environment_id, 999, '', traceback.format_exc())
        environment.state = 'FAILED'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
    else:
        environment.state = 'DESTROYED'
        from pstate.models import ProblemEnvironment
        problem_environment = ProblemEnvironment.objects.get(environment=environment)
        problem_environment.state = 'DELETED'
        problem_environment.save()
    finally:
        environment.is_locked = False
        environment.save()
        NotificationQueue.objects.create(environment=environment)


@app.task
def direct_apply(environment_id, terraform_file_id, var):
    """
    copy_tf_files ~ init ~ plan ~ applyの処理を一括して実行します.
    :param environment_id:  環境ID
    :param terraform_file_id:   terraformファイルID
    :param var: terraformコマンド実行時に引数に渡す変数
    """
    FAILED_STATUS_CODE = [1, ]
    prepare_environment(environment_id, terraform_file_id)
    from pstate.models import NotificationQueue

    from terraform_manager.models import Environment
    environment = Environment.objects.get(id=environment_id)
    environment.is_locked = True
    environment.save()
    try:
        #   terraform init
        environment.state = 'IN_INITIALIZE'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.init()
        save_log(environment_id, return_code, stdout, stderr)
        environment.state = 'INITIALIZED'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
        if return_code in FAILED_STATUS_CODE:
            raise Exception("terraformが異常終了したためtaskを停止します")

        #   terraform plan
        environment.state = 'IN_PLANNING'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.plan(var=var)
        save_log(environment_id, return_code, stdout, stderr)
        environment.state = 'PLANNED'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
        if return_code in FAILED_STATUS_CODE:
            raise Exception("terraformが異常終了したためtaskを停止します")

        #   terraform apply
        environment.state = 'IN_APPLYING'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
        import os
        os.environ["TF_CLI_ARGS"] = "-parallelism=4 -auto-approve=true"
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.apply(var=var, skip_plan=True)
        os.environ.pop("TF_CLI_ARGS")
        save_log(environment_id, return_code, stdout, stderr)
        if return_code in FAILED_STATUS_CODE:
            raise Exception("terraformが異常終了したためtaskを停止します")

        #   terraform output vnc_global_ip
        cmd = ['terraform', 'output', 'vnc_global_ip']
        import subprocess
        os.chdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code, stdout, stderr = result.returncode, result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
        from pstate.models import ProblemEnvironment
        problem_environment = ProblemEnvironment.objects.get(environment=environment)
        problem_environment.vnc_server_ipv4_address = stdout.strip()
        save_log(environment_id, return_code, stdout, stderr)
        if return_code in FAILED_STATUS_CODE:
            raise Exception("terraformが異常終了したためtaskを停止します")

        environment.state = 'APPLIED'
        environment.save()
        # TODO: 問題環境のstateが準備完了になるタイミングが一律同じでないためREADYに変更するタイミングの修正の可能性あり.
        problem_environment.state = 'READY'
        problem_environment.save()
        NotificationQueue.objects.create(environment=environment)
    except:
        import traceback
        save_log(environment_id, 999, '', traceback.format_exc())
        environment.state = 'FAILED'
        environment.save()
        NotificationQueue.objects.create(environment=environment)
    finally:
        environment.is_locked = False
        environment.save()
        import subprocess
        # tfstateを保存.
        cmd_cat = ['cat', 'terraform.tfstate']
        result = subprocess.run(cmd_cat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code, stdout, stderr = result.returncode, result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
        environment.tfstate = stdout
        environment.save()


def prepare_environment(environment_id, terraform_file_id):
    """
    terraform実行環境を作成します.
    :param environment_id:  環境ID
    :param terraform_file_id:   TerraformファイルID
    """

    # ディレクトリの作成.
    environment_dir = TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id)
    os.mkdir(environment_dir)

    # *.tfファイルのコピー.
    from terraform_manager.models import TerraformFile
    tf = TerraformFile.objects.get(id=terraform_file_id)
    f = open(environment_dir + "/" + '{}'.format(tf.file_name), 'wb')
    f.write(tf.body.encode('utf-8'))
    f.close()

    # プロバイダの設定定義ファイルの作成.
    variable_body = ''

    required_providers = """\
terraform {
  required_providers {
    sakuracloud = {
      source  = "sacloud/sakuracloud"
      version = "2.4.1"
    }
  }
}

"""

    provider_body = required_providers + 'provider {} {{\n'.format(tf.provider.provider_name)

    for attribute in tf.provider.attribute.all():
        if attribute.value is None or attribute.value == '':
            provider_body += '\t{0} = "${{var.{1}}}"\n'.format(attribute.key, attribute.key)
            variable_body += 'variable "{0}" {{}}\n'.format(attribute.key)
        else:
            provider_body += '\t{0} = "{1}"\n'.format(attribute.key, attribute.value)
    provider_body += '}\n'

    f = open(environment_dir + "/" + '{}.tf'.format(tf.provider.provider_name), 'wb')
    f.write(provider_body.encode('utf-8'))
    f.close()

    # ShellScriptのコピー
    if tf.has_shell_script():
        from terraform_manager.models import Environment
        environment = Environment.objects.get(id=environment_id)
        for script in tf.shell_script.all():
            f = open(environment_dir + "/" + '{}'.format(script.file_name), 'wb')
            script.body = script.body.replace('@@VNC_SERVER_PASSWORD@@',
                                              environment.problem_environment.all()[0].vnc_server_password)
            f.write(script.body.encode('utf-8'))
            f.close()

    # 変数定義ファイルの作成(DBに保存されているもの).
    if tf.has_variable():
        for variable in tf.variables.all():
            if variable.value is None or variable.value == '':
                variable_body += 'variable "{0}" {{}}\n'.format(variable.key)
            else:
                variable_body += 'variable "{0}" {{ default = "{1}" }}\n'.format(variable.key, variable.value)
        f = open(environment_dir + '/variables.tf', 'wb')
        f.write(variable_body.encode('utf-8'))
        f.close()


def save_log(environment_id, return_code, stdout, stderr):
    """
    ログを保存します.
    :param environment_id:
    :param return_code:
    :param stdout:
    :param stderr:
    """
    from terraform_manager.models import Log, Environment
    log = Log(environment=Environment.objects.get(id=environment_id),
              return_code=return_code,
              stdout=stdout,
              stderr=stderr)
    log.save()
