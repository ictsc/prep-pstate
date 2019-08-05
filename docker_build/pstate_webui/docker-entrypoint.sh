#!/usr/bin/env bash

set -ex

if [ "$MODE" = "web" ]; then
    gunicorn ictsc_prep_school.wsgis.pstate -b 0.0.0.0:80 -w 6 --timeout 30 --graceful-timeout 20 --max-requests 1000 --max-requests-jitter 500 --backlog 500 --access-logfile - --error-logfile -
elif [ "$MODE" = "init" ]; then
    python3 manage.py migrate
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('pstate', 'pstate@example.com', 'pstate')" | python3 manage.py shell
    python3 manage.py loaddata fixtures/terraform_manager/attribute.json
    python3 manage.py loaddata fixtures/terraform_manager/provider.json
    python3 manage.py loaddata fixtures/terraform_manager/filetemplate.json
else
    echo "error"
fi