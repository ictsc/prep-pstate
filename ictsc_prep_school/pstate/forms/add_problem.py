from django import forms

from pstate.models import Problem


class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('name', 'display_name', 'description', 'start_date', 'end_date', 'is_enabled', )
