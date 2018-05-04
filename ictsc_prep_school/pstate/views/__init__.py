from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from pstate.models import Participant

from pstate.forms.add_participant import ParticipantForm


def login(request):
    return render(request, 'admin_pages/auth/login.html')


#@login_required
def index(request):
    return render(request, 'admin_pages/index.html')


class ParticipantListView(ListView):

    model = Participant
    paginate_by = 100
    template_name = 'admin_pages/participant/index.html'

class ParticipantCreateView(CreateView):

    form_class = ParticipantForm
    template_name = 'admin_pages/participant/add.html'
    success_url = '/manage/participants/'