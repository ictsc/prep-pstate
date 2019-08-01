from django.contrib import admin

from pstate.models import Team, Participant, Problem, ProblemEnvironment, User

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Participant)

admin.site.register(Problem)
admin.site.register(ProblemEnvironment)
