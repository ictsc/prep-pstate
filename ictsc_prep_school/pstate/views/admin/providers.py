from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from pstate.forms.providers import ProviderForm
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin
from terraform_manager.models import Provider, Attribute


class ProviderCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = ProviderForm
    template_name = 'admin_pages/setting/provider/add.html'
    success_url = "/pstate/manage/setting/providers/"


class ProviderListView(LoginRequiredAndPermissionRequiredMixin, ListView):
    model = Provider
    paginate_by = 100
    template_name = 'admin_pages/setting/provider/index.html'

    def get_queryset(self):
        return super().get_queryset().order_by('id')


class ProviderDetailView(LoginRequiredAndPermissionRequiredMixin, DetailView):
    model = Provider
    paginate_by = 100
    template_name = 'admin_pages/setting/provider/detail.html'


class ProviderUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Provider
    fields = '__all__'
    template_name = 'admin_pages/common/edit.html'
    success_url = '/pstate/manage/setting/providers/'


class ProviderDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = Provider
    template_name = 'admin_pages/setting/provider/delete.html'
    success_url = '/pstate/manage/setting/providers/'


class AttributeCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    model = Attribute
    fields = '__all__'
    template_name = 'admin_pages/setting/attribute/add.html'
    success_url = '/pstate/manage/setting/attributes'


class AttributeListView(LoginRequiredAndPermissionRequiredMixin, ListView):
    model = Attribute
    paginate_by = 100
    template_name = 'admin_pages/setting/attribute/index.html'

    def get_queryset(self):
        return super().get_queryset().order_by('id')


class AttributeUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Attribute
    fields = '__all__'
    template_name = 'admin_pages/common/edit.html'
    success_url = '/pstate/manage/setting/attributes'


class AttributeDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = Attribute
    template_name = 'admin_pages/common/delete.html'
    success_url = '/pstate/manage/setting/attributes'
