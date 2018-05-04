from django import forms

from pstate.models import Team


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('__all__')
