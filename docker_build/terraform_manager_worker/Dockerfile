FROM centos:centos8

ENV PYTHONPATH /pstate/ictsc_prep_school:$PYTHONPATH
ENV DJANGO_SETTINGS_MODULE ictsc_prep_school.settings.terraform_manager.develop

RUN mkdir /terraform-manager
# terraform実行環境のディレクトリを作成.
RUN mkdir /terraform-environment

# terraformのインストール
WORKDIR /bin/
RUN yum install -y curl unzip python3-devel gcc
RUN curl -sL https://releases.hashicorp.com/terraform/0.11.14/terraform_0.11.14_linux_amd64.zip > terraform.zip
RUN unzip terraform.zip
RUN curl -sL https://github.com/sacloud/terraform-provider-sakuracloud/releases/download/v1.16.4/terraform-provider-sakuracloud_1.16.4_linux-amd64.zip > terraform_sackuracloud.zip
RUN unzip terraform_sackuracloud.zip

# ライブラリのインストール.
WORKDIR /terraform-manager/
COPY ./requirements.txt /terraform-manager/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# ソースファイルのコピー.
COPY ./ /pstate/
WORKDIR /pstate/ictsc_prep_school/
CMD watchmedo auto-restart -- celery -A terraform_manager.terraform_manager_tasks worker --loglevel=info --concurrency 8

#   TODO    :   redisとDB接続先とterraform実行環境のパスを外部から変数として設定できるようにする.
