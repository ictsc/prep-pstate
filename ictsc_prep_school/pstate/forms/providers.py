from django import forms
from django.forms import SelectMultiple

from terraform_manager.models import Provider


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'provider_name': forms.TextInput(attrs={'class': "form-control"}),
        }
