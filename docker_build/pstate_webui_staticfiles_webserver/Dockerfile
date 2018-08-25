FROM nginx

# Python3実行環境のインストール.
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ADD ./requirements.txt /root/
WORKDIR /root/
RUN pip3 install -r requirements.txt

ADD ./ictsc_prep_school /root/

ENV DJANGO_SETTINGS_MODULE ictsc_prep_school.settings.pstate.develop
ADD ./libs /root/ictsc_prep_school/settings/pstate/static
RUN python3 manage.py collectstatic --noinput

ADD docker_build/pstate_webui_staticfiles_webserver/server.conf /etc/nginx/conf.d/default.conf
ADD docker_build/pstate_webui_staticfiles_webserver/nginx.conf /etc/nginx/nginx.conf

RUN mkdir /root/logs
RUN mkdir -p /root/public/pstate-static/
RUN cp -r /root/ictsc_prep_school/settings/pstate/static/* /root/public/pstate-static/
RUN chmod 755 -R /root

CMD ["nginx", "-g", "daemon off;"]