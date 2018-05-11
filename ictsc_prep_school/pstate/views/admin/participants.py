from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from pstate.forms.participants import ParticipantForm, ParticipantUpdateForm
from pstate.models import Participant
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin


class ParticipantCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = ParticipantForm
    template_name = 'admin_pages/participant/add.html'
    success_url = '/manage/participants/'


class ParticipantListView(LoginRequiredAndPermissionRequiredMixin, ListView):
    model = Participant
    paginate_by = 100
    template_name = 'admin_pages/participant/index.html'


class ParticipantDetailView(LoginRequiredAndPermissionRequiredMixin, DetailView):
    model = Participant
    template_name = 'admin_pages/participant/detail.html'


class ParticipantUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Participant
    form_class = ParticipantUpdateForm
    template_name = 'admin_pages/participant/edit.html'
    success_url = '/manage/participants/'


class ParticipantDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = Participant
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/participants/'
