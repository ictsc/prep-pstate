from django.conf.urls import url
from django.urls import path

from pstate import views

from pstate.views import ParticipantListView, ParticipantCreateView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    url(r'^participants/$', ParticipantListView.as_view(), name='participant-list'),
    url(r'^participants/add/$', ParticipantCreateView.as_view(), name='participant-add'),

]
