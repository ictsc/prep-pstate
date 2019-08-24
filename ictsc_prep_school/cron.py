# coding:UTF-8
import logging
from traceback import format_exc

import django
import os
import time


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ictsc_prep_school.settings.pstate.develop")
django.setup()
from django.core.management import call_command

logger = logging.getLogger('django.server')


def job():
    try:
        call_command("problem_env_status_notify_to_score_server")
    except:
        logging.error(format_exc())


while True:
    from terraform_manager.models import Setting
    setting = Setting.objects.filter(name='notify_worker_notify_interval_seconds').first()
    if setting:
        pstate_notify_worker_notify_interval_seconds = int(setting.value)
    else:
        pstate_notify_worker_notify_interval_seconds = 30

    job()
    time.sleep(pstate_notify_worker_notify_interval_seconds)
