from django import forms

from terraform_manager.models import Provider


class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = ('__all__')
