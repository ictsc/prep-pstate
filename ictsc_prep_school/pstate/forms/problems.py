from django import forms

from pstate.models import Problem


class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('name', 'display_name', 'description', 'mode', 'start_date', 'end_date', )
        # fields = ('name', 'display_name', 'description', 'start_date', 'end_date', 'is_enabled', )
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'display_name': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
            'start_date': forms.TextInput(attrs={'class': "form-control datetime"}),
            'end_date': forms.TextInput(attrs={'class': "form-control datetime"}),
        }


class ProblemUpdateForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('name', 'display_name', 'mode', 'start_date', 'end_date', )
        # fields = ('name', 'display_name', 'description', 'start_date', 'end_date', 'is_enabled', )
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'display_name': forms.TextInput(attrs={'class': "form-control"}),
        }


class ProblemEnvironmentCreateExecuteForm(forms.Form):
    pass


class ProblemEnvironmentDestroyExecuteForm(forms.Form):
    pass

class ProblemEnvironmentGroupDestroyDeleteExecuteForm(forms.Form):
    pass

class ProblemEnvironmentRecreateExecuteForm(forms.Form):
    pass


class ProblemDescriptionUpdateForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('description', )
        widgets = {
            'description': forms.Textarea(attrs={'class': "form-control"}),
        }


class ProblemStartForm(forms.Form):
    pass


class ProblemEndForm(forms.Form):
    pass
