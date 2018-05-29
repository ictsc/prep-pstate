FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y curl nginx python3 python3-pip

ADD ./requirements.txt /root/
WORKDIR /root/
RUN pip3 install -r requirements.txt

ADD ./ictsc_prep_school /root/

ENV DJANGO_SETTINGS_MODULE ictsc_prep_school.settings.pstate.develop
ADD ./libs /root/ictsc_prep_school/settings/pstate/static
RUN python3 manage.py collectstatic --noinput
CMD ["uwsgi","--http",":80","--file","/root/ictsc_prep_school/wsgis/pstate.py"]