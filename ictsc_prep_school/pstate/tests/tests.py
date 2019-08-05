from django.test import TestCase, Client
from pstate.models import ProblemEnvironment, Problem
from terraform_manager.models import Environment, TerraformFile, Provider, Attribute
from django.contrib.auth import get_user_model

# Create your tests here.

def create_test_tf_file():
    tf_file = TerraformFile(name="test_tf_file", body="test", file_name="test_name", provider=Provider.objects.all()[0])
    tf_file.save()
    return tf_file

def create_test_environment(tf_file):
    environment = Environment(terraform_file=tf_file, state="IN_PLANNING")
    environment.save()
    return environment

def create_test_problem(tf_file):
    problem = Problem(name="test_name", display_name="test_display_name", terraform_file_id = tf_file)
    problem.save()
    return problem

def create_test_problem_environment(environment, problem):
    problem_environment = ProblemEnvironment(vnc_server_ipv4_address="192.168.0.1", environment=environment, problem=problem, is_enabled = True)
    problem_environment.save()
    return problem_environment


# View Tests
class ProblemEnvironmentListViewTests(TestCase):
    fixtures = [ 'fixtures/terraform_manager/attribute.json', 'fixtures/terraform_manager/provider.json' ]

    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser('pstate', 'pstate@example.com', 'pstate')
        self.client = Client()
        self.client.login(username='pstate', password='pstate')

    def test_get_queryset(self):   
        pass
    def test_get_context_data(self):
        pass

    def test_one_bulk_destroy_post(self):
        test_tf_file = create_test_tf_file()
        test_environment =  create_test_environment(test_tf_file)
        test_problem = create_test_problem(test_tf_file)
        test_problem_environment = create_test_problem_environment(test_environment, test_problem)
        test_problem_environment_count = ProblemEnvironment.objects.count()
        response = self.client.post("/pstate/manage/problem_environments/", {"problem_id": "1", "destroy": "destroy"})
        response = self.client.post(response.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_problem_environment_count, ProblemEnvironment.objects.count())

    def test_no_data_bulk_destroy_post(self):
        pass

    def test_one_bulk_delete_post(self):
        test_tf_file = create_test_tf_file()
        test_environment =  create_test_environment(test_tf_file)
        test_problem = create_test_problem(test_tf_file)
        test_problem_environment = create_test_problem_environment(test_environment, test_problem)
        test_problem_environment_count = ProblemEnvironment.objects.count()
        response = self.client.post("/pstate/manage/problem_environments/", {"problem_id": "1", "delete": "delete"})
        response = self.client.post(response.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_problem_environment_count - 1, ProblemEnvironment.objects.count())
  
    def test_no_data__bulk_delete_post(self):
        pass

class ProblemEnvironmentDestroyViewTests(TestCase):

    def test_one_form_valid(self):
        pass

    def test_terraform_destroy(self):
        pass


