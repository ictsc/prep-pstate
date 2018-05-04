from django import forms

from pstate.models import Participant


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant
        fields = ('__all__')