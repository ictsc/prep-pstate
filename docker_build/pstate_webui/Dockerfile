FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y curl nginx python3 python3-pip gettext

ADD ./requirements.txt /root/
WORKDIR /root/
RUN pip3 install -r requirements.txt

ADD ./ictsc_prep_school /root/

ENV DJANGO_SETTINGS_MODULE ictsc_prep_school.settings.pstate.develop
ADD ./libs /root/ictsc_prep_school/settings/pstate/static
RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py compilemessages
CMD ["uwsgi","-p","6","--http",":80","--file","/root/ictsc_prep_school/wsgis/pstate.py"]
