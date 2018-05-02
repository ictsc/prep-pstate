from django.conf.urls import url
from django.urls import include

from . import views

app_name = 'terraform_manager'

urlpatterns = [
    url(r'', include(views.urlpatterns))
]
