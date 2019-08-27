#!/usr/bin/env bash

set -x

VERSION="20190827020"

PSTATE_WEB_VERSION="pstate_webui:${VERSION}"
PSTATE_STATIC_SERVER_VERSION="pstate-static-server:${VERSION}"
TERRAFORM_MANAGER_VERSION="terraform-manager-worker:${VERSION}"

docker build -t ${PSTATE_WEB_VERSION} -f docker_build/pstate_webui/Dockerfile .
docker build -t ${PSTATE_STATIC_SERVER_VERSION} -f docker_build/pstate_webui_staticfiles_webserver/Dockerfile .
docker build -t ${TERRAFORM_MANAGER_VERSION} -f docker_build/terraform_manager_worker/Dockerfile .

shopt -s expand_aliases

if sed --version 2>/dev/null | grep -q GNU; then
  alias sedi='sed -i '
else
  alias sedi='sed -i "" '
fi

sedi -e "s/PSTATE_IMAGE/${PSTATE_WEB_VERSION}/g" ./manifest/helm/pstate.yaml
sedi -e "s/TERRAFORM_MANAGER_WORKER_IMAGE/${TERRAFORM_MANAGER_VERSION}/g" ./manifest/helm/pstate-worker.yaml
sedi -e "s/PSTATE_IMAGE/${PSTATE_WEB_VERSION}/g" ./manifest/helm/pstate-notify-worker.yaml
sedi -e "s/PSTATE_STATIC_SERVER_IMAGE/${PSTATE_STATIC_SERVER_VERSION}/g" ./manifest/helm/pstate-staticfiles-webserver.yaml

sedi -e "s/PSTATE_VERSION/${VERSION}/g" ./ictsc_prep_school/pstate/templates/adminlte/lib/_main_footer.html
