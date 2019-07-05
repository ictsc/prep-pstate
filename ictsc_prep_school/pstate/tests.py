from django.test import TestCase
from pstate.models import ProblemEnvironment, Problem
from terraform_manager.models import Environment, TerraformFile, Provider
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
    pass

class ProblemEnvironmentDestroyViewTests(TestCase):
    pass