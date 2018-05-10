from django import forms

from pstate.models import Problem


class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('name', 'display_name', 'description', 'is_enabled', )
        # fields = ('name', 'display_name', 'description', 'start_date', 'end_date', 'is_enabled', )
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'display_name': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
            #'start_date': forms.DateTimeField(attrs={'class': "form-control"}),
        }


class ProblemEnvironmentCreateExecuteForm(forms.Form):
    pass


class ProblemDescriptionUpdateForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('description', )
        widgets = {
            'description': forms.Textarea(attrs={'class': "form-control"}),
        }
