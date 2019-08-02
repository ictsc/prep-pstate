from django import forms
from django.forms import SelectMultiple

from pstate.models import Github


class GithubForm(forms.ModelForm):
    class Meta:
        model = Github
        fields = '__all__'
        widgets = {
            'secret_key': forms.TextInput(attrs={'class': "form-control"}),
        }

class GithubUpdateForm(forms.ModelForm):
    class Meta:
        model = Github
        fields= ['name',
                'git_source',
                'project_root_path',
                'teams_file', 
                'problem_path'
                ]
        exclude = ['ssh_private_key']
