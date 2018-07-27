from django import forms

from pstate.models import ProblemEnvironment, Team


class ProblemEnvironmentForm(forms.ModelForm):

    teams = forms.ModelMultipleChoiceField(
        label='問題環境を作成するチーム',
        queryset=Team.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = ProblemEnvironment
        fields = []


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
