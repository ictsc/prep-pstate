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
