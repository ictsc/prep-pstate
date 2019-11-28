#!/usr/bin/env bash

set -x

# pstate全体のバージョン
VERSION="20191127023"

REPOSITORY="ictscprepschool/pstate"

# pstateのコンポーネントごとにimageが異なるので末尾にバージョンを付加する
PSTATE_WEB_VERSION="pstate_webui-${VERSION}"
PSTATE_STATIC_SERVER_VERSION="pstate-static-server-${VERSION}"
TERRAFORM_MANAGER_VERSION="terraform-manager-worker-${VERSION}"

# pstateのwebuiにバージョンを入れるためビルド前に置換する
sedi -e "s/PSTATE_VERSION/${VERSION}/g" ./ictsc_prep_school/pstate/templates/adminlte/lib/_main_footer.html

docker build -t ${PSTATE_WEB_VERSION} -f docker_build/pstate_webui/Dockerfile .
docker build -t ${PSTATE_STATIC_SERVER_VERSION} -f docker_build/pstate_webui_staticfiles_webserver/Dockerfile .
docker build -t ${TERRAFORM_MANAGER_VERSION} -f docker_build/terraform_manager_worker/Dockerfile .

docker tag ${PSTATE_WEB_VERSION} ${REPOSITORY}:${PSTATE_WEB_VERSION}
docker tag ${PSTATE_STATIC_SERVER_VERSION} ${REPOSITORY}:${PSTATE_STATIC_SERVER_VERSION}
docker tag ${TERRAFORM_MANAGER_VERSION} ${REPOSITORY}:${TERRAFORM_MANAGER_VERSION}

docker login --username=ictscprepschool --password="iCtsC2O18"

docker push ${REPOSITORY}:${PSTATE_WEB_VERSION}
docker push ${REPOSITORY}:${PSTATE_STATIC_SERVER_VERSION}
docker push ${REPOSITORY}:${TERRAFORM_MANAGER_VERSION}
