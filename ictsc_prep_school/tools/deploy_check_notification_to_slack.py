import time

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

PSTATE_API_URL = 'https://prep.icttoracon.net/pstate/manage/api/problem_environments/'
PSTATE_API_USERNAME = ''
PSTATE_API_PASSWORD = ''

WEB_HOOK_URL = ""

BODY_TEMPLATE = """
```実行待ち: {in_waiting}
実行中: {in_applying}
完了: {applied}
失敗: {failed}
削除中: {in_destroying}
削除完了: {destroyed}

進捗: {progress}%
エラー: {error_rate}%
```
"""


def get_problem_environment():
    response = requests.get(url=PSTATE_API_URL, auth=(PSTATE_API_USERNAME, PSTATE_API_PASSWORD), verify=False)
    response.raise_for_status()
    return response.json()


def show_problem_environment_status(problem_environment):
    buff = "```"
    wait = 0
    for env in problem_environment:
        if env['terraform_state'] == '問題環境作成開始待ち':
        # if env['terraform_state'] == 'IN_WAITING_FOR_START':
            wait = wait + 1
            print(env["id"])
    print("IN_WAITING_FOR_START task: {}".format(wait))
    buff = buff + "IN_WAITING_FOR_START task: {}".format(wait) + "\n"

    in_applying = 0
    for env in problem_environment:
        if env['terraform_state'] == 'IN_APPLYING':
            in_applying = in_applying + 1
    print("IN_APPLYING task: {}".format(in_applying))
    buff = buff + "IN_APPLYING task: {}".format(in_applying) + "\n"

    applied = 0
    for env in problem_environment:
        if env['terraform_state'] == 'APPLIED':
            applied = applied + 1
    print("APPLIED task: {}".format(applied))
    buff = buff + "APPLIED task: {}".format(applied) + "\n"

    failed = 0
    for env in problem_environment:
        if env['terraform_state'] == 'FAILED':
            failed = failed + 1
    print("FAILED task: {}".format(failed))
    buff = buff + "FAILED task: {}".format(failed) + "\n"

    in_destroying = 0
    for env in problem_environment:
        if env['terraform_state'] == 'IN_DESTROYING':
            in_destroying = in_destroying + 1
    print("IN_DESTROYING task: {}".format(in_destroying))
    buff = buff + "IN_DESTROYING task: {}".format(in_destroying) + "\n"

    destroyed = 0
    for env in problem_environment:
        if env['terraform_state'] == 'DESTROYED':
            destroyed = destroyed + 1
    print("DESTROYED task: {}".format(destroyed))
    buff = buff + "DESTROYED task: {}".format(destroyed) + "\n"

    total = wait + in_applying + applied + failed + in_destroying + destroyed
    print('進捗: ' + str(applied / total * 100))
    buff = buff + '進捗: ' + str(applied / total * 100) + "\n"
    print('エラーレート: ' + str(failed / total * 100))
    buff = buff + 'エラーレート: ' + str(failed / total * 100) + "\n```"
    print("-------------")
    print(buff)
    import json
    d = {
        "in_waiting": wait,
        "in_applying": in_applying,
        "applied": applied,
        "failed": failed,
        "in_destroying": in_destroying,
        "destroyed": destroyed,
        "progress": str(applied / total * 100),
        "error_rate": str(failed / total * 100),
         }
    body = BODY_TEMPLATE.format(**d)
    requests.post(WEB_HOOK_URL, data=json.dumps({
        'text': body,  # 通知内容
        'username': 'ictsc deploy bot',  # ユーザー名
        'icon_emoji': ':smile_cat:',  # アイコン
        'link_names': 1,  # 名前をリンク化
    }))


if __name__ == "__main__":
    result = get_problem_environment()
    show_problem_environment_status(problem_environment=result)
