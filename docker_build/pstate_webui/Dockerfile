FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y curl nginx python3 python3-pip gettext
ADD ./requirements.txt /root/
WORKDIR /root/
RUN pip3 install -r requirements.txt
ADD ./ictsc_prep_school /root/
ADD ./libs /root/ictsc_prep_school/settings/pstate/static
RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py compilemessages
RUN mkdir ~/.ssh/
RUN ssh-keygen -F github.com || ssh-keyscan github.com >> ~/.ssh/known_hosts
COPY ./docker_build/pstate_webui/docker-entrypoint.sh /root/entrypoint.sh
RUN chmod 755 /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]

EXPOSE 80
