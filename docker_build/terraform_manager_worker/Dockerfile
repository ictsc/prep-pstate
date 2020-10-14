FROM centos:centos8

ENV PYTHONPATH /pstate/ictsc_prep_school:$PYTHONPATH
ENV DJANGO_SETTINGS_MODULE ictsc_prep_school.settings.terraform_manager.develop

# terraform実行環境のディレクトリを作成.
RUN mkdir /terraform-environment

WORKDIR /bin/
RUN yum install -y curl unzip python3-devel gcc

# terraformのインストール
RUN curl -sL https://releases.hashicorp.com/terraform/0.13.3/terraform_0.13.3_linux_amd64.zip > tmp.zip \
  && unzip tmp.zip \
  && rm tmp.zip \
  && mv ./terraform /usr/local/bin/

# sakuracloud provider
RUN mkdir -p /root/.terraform.d/plugins/registry.terraform.io/sacloud/sakuracloud/2.4.1/linux_amd64
WORKDIR /root/.terraform.d/plugins/registry.terraform.io/sacloud/sakuracloud/2.4.1/linux_amd64
RUN curl -sL https://github.com/sacloud/terraform-provider-sakuracloud/releases/download/v2.4.1/terraform-provider-sakuracloud_2.4.1_linux_amd64.zip > tmp.zip \
  && unzip tmp.zip \
  && rm tmp.zip

# ライブラリのインストール.
RUN mkdir /terraform-manager
WORKDIR /terraform-manager/
COPY ./requirements.txt /terraform-manager/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# ソースファイルのコピー.
COPY ./ /pstate/
WORKDIR /pstate/ictsc_prep_school/
CMD watchmedo auto-restart -- celery -A terraform_manager.terraform_manager_tasks worker --loglevel=info --concurrency 8

#   TODO    :   redisとDB接続先とterraform実行環境のパスを外部から変数として設定できるようにする.
