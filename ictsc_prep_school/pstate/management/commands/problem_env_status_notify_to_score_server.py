import requests
from django.conf import settings
from django.core.management import BaseCommand

MUTATION_TEMPLATE_ADD_PROBLEM_ENV = '''
mutation {
    applyProblemEnvironment(input: {
        problemCode: "{problem_code}", teamNumber: {team_number},
        status: "{status}", host: "{host}",
        user: "{vnc_login_username}", password: "{vnc_login_password}" }
    ) {

    errors
  }
}
'''


class Command(BaseCommand):
    help = 'スコアサーバに問題環境の状態を通知します.'

    def __init__(self):
        super().__init__()
        self.url = settings.SCORE_SERVER_API_URL
        self.auth_url = self.url + '/api/sessions'
        self.graphql_url = self.url + '/api/graphql'
        self.user_name = settings.SCORE_SERVER_AUTH_USER_NAME
        self.password = settings.SCORE_SERVER_AUTH_PASSWORD
        self.session = requests.Session()

    def handle(self, *args, **options):
        self.__login_score_server()
        self.__request_to_score_server()
        self.__logout_score_server()

    def __login_score_server(self):
        data = {"name": self.user_name, "password": self.password}
        response = self.session.post(url=self.auth_url, data=data, timeout=5)
        response.raise_for_status()

    def __logout_score_server(self):
        response = self.session.delete(url=self.auth_url, timeout=5)
        response.raise_for_status()

    def __request_to_score_server(self):
        mutation = '''
        mutation {
            applyProblemEnvironment(input: {
                problemCode: "AAA", teamNumber: 1,
                status: "dummy status3", host: "192.168.0.1",
                user: "ubuntu", password: "ubuntu" }
            ) {
            
            errors
          }
        }
        '''
        data = {"query": mutation}
        response = self.session.post(url=self.graphql_url, data=data, timeout=5)
        response.raise_for_status()
        if response.json()['data']['applyProblemEnvironment']['errors']:
            raise Exception("API Error {}".format(response.content))
