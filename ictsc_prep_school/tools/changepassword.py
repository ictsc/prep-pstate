import random
import string

import yaml
import sys


def password_generator(size=8, chars=string.ascii_letters + string.digits):
    """
    Returns a string of random characters, useful in generating temporary
    passwords for automated password resets.

    size: default=8; override to provide smaller/larger passwords
    chars: default=A-Za-z0-9; override to provide more/less diversity

    Credit: Ignacio Vasquez-Abrams
    Source: http://stackoverflow.com/a/2257449
    """
    return ''.join(random.choice(chars) for i in range(size))


def change_team_password():
    import yaml
    data = yaml.load(open("./password.yaml"))
    from pstate.models import Team
    for team in data["teams"]["prep1"]:
        team_instance = Team.objects.get(username=team["name"])
        team_instance.set_password(team["password"])
        team_instance.save()
    return data


def change_user_password():
    import yaml
    data = yaml.load(open("./password.yaml"))
    from django.contrib.auth import get_user_model
    User = get_user_model()
    for team in data["teams"]["prep1"]:
        team_instance = User.objects.get(username=team["name"])
        team_instance.set_password(team["password"])
        team_instance.save()
    return data


def generate_new_password():
    data = yaml.load(open(sys.argv[1]))
    for team in data["teams"]["prep1"]:
        new_password = password_generator()
        team["password"] = new_password
        # team = Team.objets.get(team_name=team["name"])
        # team.set_password(new_password)
        # team.save()
    return data


if __name__ == "__main__":
    # print(generate_new_password())
    data = generate_new_password()
    change_team_password(data)
