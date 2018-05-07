from django import forms

from pstate.models import ProblemEnvironment


class ProblemEnvironmentForm(forms.ModelForm):

    class Meta:
        model = ProblemEnvironment
        fields = ('__all__')
