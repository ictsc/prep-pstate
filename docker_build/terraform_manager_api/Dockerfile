FROM ubuntu:16.04

# Python3実行環境のインストール.
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev curl nginx \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# ライブラリのインストール.
RUN mkdir /pstate
WORKDIR /pstate/
COPY ./requirements.txt /pstate/
RUN pip3 install -r requirements.txt

# ソースファイルのコピー.
COPY ./ /pstate/

ENV PYTHONPATH /pstate/ictsc_prep_school:$PYTHONPATH
WORKDIR /pstate/ictsc_prep_school
CMD ["uwsgi","--http",":80","--file","/pstate/ictsc_prep_school/ictsc_prep_school/wsgis/terraform_manager.py"]