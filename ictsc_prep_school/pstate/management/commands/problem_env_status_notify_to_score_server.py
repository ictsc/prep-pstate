import logging

import requests
from django.conf import settings
from django.core.management import BaseCommand

from pstate.models import NotificationQueue


class Command(BaseCommand):
    help = 'スコアサーバに問題環境の状態を通知します.'

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('django.server')
        self.url = settings.SCORE_SERVER_API_URL
        self.auth_url = self.url + '/api/sessions'
        self.graphql_url = self.url + '/api/graphql'
        self.user_name = settings.SCORE_SERVER_AUTH_USER_NAME
        self.password = settings.SCORE_SERVER_AUTH_PASSWORD
        self.session = requests.Session()

    def handle(self, *args, **options):
        if len(NotificationQueue.objects.all()) != 0:
            self.__login_score_server()
        for notification in NotificationQueue.objects.all().order_by('created_at'):
            try:
                if self.__request_to_score_server(notification.payload):
                    notification.delete()
            except:
                pass
        if len(NotificationQueue.objects.all()) != 0:
            self.__logout_score_server()

    def __login_score_server(self):
        data = {"name": self.user_name, "password": self.password}
        response = self.session.post(url=self.auth_url, data=data, timeout=5)
        response.raise_for_status()

    def __logout_score_server(self):
        response = self.session.delete(url=self.auth_url, timeout=5)
        response.raise_for_status()

    def __request_to_score_server(self, mutation):
        data = {"query": mutation}
        self.logger.info("Request to score server {}".format(mutation))
        response = self.session.post(url=self.graphql_url, data=data, timeout=5)
        response.raise_for_status()
        if 'errors' in response.json() and response.json()['errors'] != []:
            self.logger.error("API Error {}, {}".format(response.content, mutation))
            raise Exception("API Error")
        return True
