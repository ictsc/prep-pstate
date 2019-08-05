# coding:UTF-8
import django
import os
import time

import schedule


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ictsc_prep_school.settings.pstate.develop")
django.setup()
from django.core.management import call_command


def job():
    try:
        print(call_command("problem_env_status_notify_to_score_server"))
    except:
        pass


schedule.every(1).seconds.do(job)

while True:
    schedule.run_pending()
    from terraform_manager.models import Setting
    setting = Setting.objects.filter(name='notify_worker_notify_interval_seconds').first()
    if setting:
        pstate_notify_worker_notify_interval_seconds = int(setting.value)
    else:
        pstate_notify_worker_notify_interval_seconds = 30
    time.sleep(pstate_notify_worker_notify_interval_seconds)
