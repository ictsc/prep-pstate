import time

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

PSTATE_API_URL = 'https://prep.icttoracon.net/pstate/manage/api/problem_environments/'
PSTATE_API_USERNAME = ''
PSTATE_API_PASSWORD = ''


def get_problem_environment():
    response = requests.get(url=PSTATE_API_URL, auth=(PSTATE_API_USERNAME, PSTATE_API_PASSWORD), verify=False)
    response.raise_for_status()
    return response.json()


def show_problem_environment_status(problem_environment):
    wait = 0
    for env in problem_environment:
        if env['terraform_state'] == '問題環境作成開始待ち':
            wait = wait + 1
            print(env["id"])
    print("IN_WAITING_FOR_START task: {}".format(wait))

    in_applying = 0
    for env in problem_environment:
        if env['terraform_state'] == 'IN_APPLYING':
            in_applying = in_applying + 1
    print("IN_APPLYING task: {}".format(in_applying))

    applied = 0
    for env in problem_environment:
        if env['terraform_state'] == 'APPLIED':
            applied = applied + 1
    print("APPLIED task: {}".format(applied))

    failed = 0
    for env in problem_environment:
        if env['terraform_state'] == 'FAILED':
            failed = failed + 1
    print("FAILED task: {}".format(failed))

    in_destroying = 0
    for env in problem_environment:
        if env['terraform_state'] == 'IN_DESTROYING':
            in_destroying = in_destroying + 1
    print("IN_DESTROYING task: {}".format(in_destroying))

    destroyed = 0
    for env in problem_environment:
        if env['terraform_state'] == 'DESTROYED':
            destroyed = destroyed + 1
    print("DESTROYED task: {}".format(destroyed))

    total = wait + in_applying + applied + failed + in_destroying + destroyed
    print('進捗: ' + str(applied / total * 100))
    print('エラーレート: ' + str(failed / total * 100))


if __name__ == "__main__":
    while True:
        result = get_problem_environment()
        show_problem_environment_status(problem_environment=result)
        time.sleep(1)
