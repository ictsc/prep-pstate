from django import forms

from terraform_manager.models import Provider


class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'provider_name': forms.TextInput(attrs={'class': "form-control"}),
            # 'attribute': forms.ModelMultipleChoiceField(queryset=None),
        }
