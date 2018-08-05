#!/usr/bin/env bash

docker build -t pstate_webui:20180804009 -f docker_build/pstate_webui/Dockerfile .
docker build -t pstate-static-server:20180705 -f docker_build/pstate_webui_staticfiles_webserver/Dockerfile .
docker build -t terraform-manager-worker:20180804008  -f docker_build/terraform_manager_worker/Dockerfile .