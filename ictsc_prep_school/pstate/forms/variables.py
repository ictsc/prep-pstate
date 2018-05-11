from django import forms

from terraform_manager.models import Variable


class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = ['key', 'value', ]
        widgets = {
            'key': forms.TextInput(attrs={'class': "form-control"}),
            'value': forms.TextInput(attrs={'class': "form-control"}),
        }


class VariableUpdateForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = ['key', 'value', ]
        widgets = {
            'key': forms.TextInput(attrs={'class': "form-control"}),
            'value': forms.TextInput(attrs={'class': "form-control"}),
        }
