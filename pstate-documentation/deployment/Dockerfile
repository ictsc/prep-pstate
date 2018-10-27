FROM nginx

# Python3実行環境のインストール.
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# ライブラリのインストール.
RUN mkdir /pstate-documentation
WORKDIR /pstate-documentation/
COPY ./requirements.txt /pstate-documentation/
RUN pip3 install -r requirements.txt
COPY ./ /pstate-documentation/
RUN make html

ADD deployment/server.conf /etc/nginx/conf.d/default.conf

RUN mkdir /root/logs
RUN mkdir -p /root/public/pstate-documentation/
RUN cp -r /pstate-documentation/_build/html/* /root/public/pstate-documentation/
RUN chmod 755 -R /root

CMD ["nginx", "-g", "daemon off;"]