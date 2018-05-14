from django import forms

from pstate.models import ProblemEnvironment


class ProblemEnvironmentForm(forms.ModelForm):

    class Meta:
        model = ProblemEnvironment
        fields = ['team', ]


class ProblemEnvironmentUpdateForm(forms.ModelForm):
    class Meta:
        model = ProblemEnvironment
        fields = ['state', 'is_enabled', ]
        exclude = ['vnc_server_ipv4_address',
                   'vnc_server_port',
                   'vnc_server_username',
                   'vnc_server_password',
                   'team',
                   'participant',
                   'environment',
                   'problem',
                   ]
