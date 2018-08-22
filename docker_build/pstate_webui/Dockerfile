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
#CMD ["uwsgi","--max-requests","1000","--max-requests-delta","300","--harakiri","20","-p","6","--http",":80","--file","/root/ictsc_prep_school/wsgis/pstate.py"]
CMD ["gunicorn", "ictsc_prep_school.wsgis.pstate", "-b", "0.0.0.0:80", "-w", "6", "--timeout", "30", "--graceful-timeout", "20", "--max-requests", "1000", "--max-requests-jitter", "500", "--backlog", "500", "--access-logfile", "-", "--error-logfile", "-"]