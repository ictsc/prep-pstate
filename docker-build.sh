#!/usr/bin/env bash

set -ex

# pstate全体のバージョン
VERSION="20191127023"

REPOSITORY="ictsc.sakuracr.jp"

# pstateのコンポーネントごとにimageが異なるので末尾にバージョンを付加する
PSTATE_WEB="pstate_webui"
PSTATE_STATIC_SERVER="pstate-static-server"
TERRAFORM_MANAGER="terraform-manager-worker"

# GNUとBSDでsedの挙動が異なるので差分を吸収する
shopt -s expand_aliases

if sed --version 2>/dev/null | grep -q GNU; then
  alias sedi='sed -i '
else
  alias sedi='sed -i "" '
fi

# pstateのwebuiにバージョンを入れるためビルド前に置換する
sedi -e "s/PSTATE_VERSION/${VERSION}/g" ./ictsc_prep_school/pstate/templates/adminlte/lib/_main_footer.html

docker build -t ${PSTATE_WEB}:${VERSION} -f docker_build/pstate_webui/Dockerfile .
docker build -t ${PSTATE_STATIC_SERVER}:${VERSION} -f docker_build/pstate_webui_staticfiles_webserver/Dockerfile .
docker build -t ${TERRAFORM_MANAGER}:${VERSION} -f docker_build/terraform_manager_worker/Dockerfile .

docker tag ${PSTATE_WEB}:${VERSION} ${REPOSITORY}/${PSTATE_WEB}:${VERSION}
docker tag ${PSTATE_STATIC_SERVER}:${VERSION} ${REPOSITORY}/${PSTATE_STATIC_SERVER}:${VERSION}
docker tag ${TERRAFORM_MANAGER}:${VERSION} ${REPOSITORY}/${TERRAFORM_MANAGER}:${VERSION}

docker login --username=ictsc --password="cQX6NWcGKexBat87" ${REPOSITORY}

docker push ${REPOSITORY}/${PSTATE_WEB}:${VERSION}
docker push ${REPOSITORY}/${PSTATE_STATIC_SERVER}:${VERSION}
docker push ${REPOSITORY}/${TERRAFORM_MANAGER}:${VERSION}
